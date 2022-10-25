from _datetime import datetime, timedelta
import json
import logging
import time

import pytz
import requests

import config as cfg
from src.api.Match_BDD import Match
from src.api.Paris_BDD import Paris
from src.api.Saisons_BDD import Saisons


## Pour les tests :
# https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:82574/lineups.json?api_key=


def get_matchs(saison_id):
    """Retourne les informations sur les matchs d'une saison.

    :param str saison_id: l'id de la saison ou on souhaite connaitre les matchs
    :rtype: list or None
    :returns: json object contenant les matchs
    """
    url = f"https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:{saison_id}/lineups.json?api_key={cfg.rygby_api_key}"

    req = requests.get(url)
    try:
        return json.loads(req.content.decode("utf-8"))["lineups"]
    except Exception as e:
        logging.warning(f"Erreur avec {url}\n retour : {req}\n{str(e)}")
        return None


def get_info_matchs(match_id):
    """Retourne les informations sur un match.

    :param str match_id: l'id du match ou on souhaite des infos
    :rtype: dict or None
    :returns: json object contenant les matchs
    """
    url = f"https://api.sportradar.us/rugby-union/trial/v3/fr/sport_events/sr:match:{match_id}/summary.json?api_key={cfg.rygby_api_key}"

    req = requests.get(url)
    try:
        return json.loads(req.content.decode("utf-8"))
    except Exception as e:
        logging.warning(f"Erreur avec {url}\n retour : {req}\n{str(e)}")
        return None


def add_match_bdd(match, saison):
    """Ajoute le match dans la base de donnee si il n'y est pas

    :param dict match: match a ajouter dans la bdd
    :rtype: None
    """
    match_id = match["sport_event"]["id"].split(":")[2]
    if Match.get_or_none(Match.match_id == match_id) is None:
        date_match = datetime.strptime(
                match["sport_event"]["start_time"], "%Y-%m-%dT%H:%M:%S%z"
                )
        match = Match(
                match_id=match_id,
                equipe1=match["sport_event"]["competitors"][0]["name"],
                equipe1_code=match["sport_event"]["competitors"][0]["id"].split(":")[2],
                equipe2=match["sport_event"]["competitors"][1]["name"],
                equipe2_code=match["sport_event"]["competitors"][1]["id"].split(":")[2],
                date_match=date_match,
                saison=saison
                )
        match.save()


def add_match():
    """Ajoute les matchs de toutes les saisons dans la BDD

    :rtype: str
    """
    for saison in Saisons.select():
        matchs = get_matchs(saison.season_id)
        if matchs is not None:
            for match in matchs:
                add_match_bdd(match, saison)
        else:
            logging.warning(f"Aucun match trouvé pour {saison.nom}")
    return "Matchs ajouté avec succès"


def liste_match():
    """Liste les matchs de la BDD

    :rtype: str
    """
    reponse = "Voici les matchs disponibles:\n"
    for match in Match.select().where(Match.date_match > datetime.now()):
        reponse += f"{match.equipe1} - {match.equipe2}\n"
    return reponse


def delete_matchs():
    for match in Match.select():
        match.delete_instance()
    return "Les matchs ont bien été supprimés"


def refresh_match():
    """Cherche les matchs qui sont passé et lance leur actualisation

    :rtype: str
    """
    for match in Match.select():
        if match.vainqueur == 0 and match.get_date_match() <= datetime.now().replace(tzinfo=pytz.UTC) and \
                (not cfg.test or match.get_date_match() <= datetime.now().replace(tzinfo=pytz.UTC) - timedelta(days=7)):
            time.sleep(5)
            actualiser_match(match)
    return "Resultats bien mis à jour"


def actualiser_match(match):
    """Actualise un match avec les scores

    :param Match match: match a actualiser
    :rtype: None
    """
    logging.info(f"Actualisation du match {match.equipe1} - {match.equipe2}")
    summary_match = get_info_matchs(match.match_id)
    if not summary_match:
        return
    if summary_match["sport_event_status"]["status"] == "closed":
        match.resultat_equipe1 = summary_match["sport_event_status"]["home_score"]
        match.resultat_equipe2 = summary_match["sport_event_status"]["away_score"]
        if "statistic" in summary_match:
            if summary_match["statistics"]["totals"]["competitors"][0]["statistics"]["tries"] > 3:
                match.bonus_offensif = True
            if summary_match["statistics"]["totals"]["competitors"][1]["statistics"]["tries"] > 3:
                match.bonus_offensif = True
        if abs(match.resultat_equipe1 - match.resultat_equipe2) < 8:
            match.bonus_defensif = True
        if match.resultat_equipe1 > match.resultat_equipe2:
            match.vainqueur = 1
        elif match.resultat_equipe2 > match.resultat_equipe1:
            match.vainqueur = 2
        else:
            match.vainqueur = 3
        match.save()
        actualiser_paris(match)


def actualiser_paris(match):
    """Actualise les paris concernant le match en question

    :param Match match: match qui necessite d'actualiser les paris
    :rtype: None
    """
    for paris in Paris.select():
        if paris.match == match:
            if paris.vainqueur == match.vainqueur:
                paris.points_gagnes += cfg.pts_paris_gagnant
            if paris.bonus_offensif and match.bonus_offensif:
                paris.points_gagnes += cfg.pts_bonus_offensif
            if paris.bonus_defensif and match.bonus_defensif:
                paris.points_gagnes += cfg.pts_bonus_defensif
            joueur = paris.joueur
            joueur.total_point += paris.points_gagnes
            joueur.save()
            paris.save()
