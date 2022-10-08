from _datetime import datetime
import json
import logging

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


def add_match_bdd(match):
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
                )
        match.save()


def add_match():
    """Ajoute les matchs de toutes les saisons dans la BDD

    :rtype: str
    """
    for saison in Saisons.select():
        matchs = get_matchs(saison.season_id)
        for match in matchs:
            add_match_bdd(match)
    return "Matchs ajouté avec succès"


def liste_match():
    """Liste les matchs de la BDD

    :rtype: str
    """
    reponse = "Voici les matchs disponibles:\n"
    for match in Match.select():
        reponse += f"{match.equipe1} - {match.equipe2}\n"
    return reponse


def refresh_match():
    """Cherche les matchs qui sont passé et lance leur actualisation

    :rtype: str
    """
    for match in Match.select():
        if match.get_date_match() <= datetime.now().replace(tzinfo=pytz.UTC):
            actualiser_match(match)
    return "Resultat bien mis à jour"


def actualiser_match(match):
    """Actualise un match avec les scores

    :param Match match: match a actualiser
    :rtype: None
    """
    summary_match = get_info_matchs(match.match_id)
    if not summary_match:
        return
    if summary_match["sport_event_status"]["status"] == "closed":
        match.resultat_equipe1 = summary_match["sport_event_status"]["home_score"]
        match.resultat_equipe2 = summary_match["sport_event_status"]["away_score"]
        if (
                summary_match["statistics"]["totals"]["competitors"][0]["statistics"][
                    "tries"
                ]
                > 3
        ):
            match.bonus_offensif = True
        if (
                summary_match["statistics"]["totals"]["competitors"][1]["statistics"][
                    "tries"
                ]
                > 3
        ):
            match.bonus_offensif = True
        if abs(match.resultat_equipe1 - match.resultat_equipe2) < 8:
            match.bonus_defensif = True
        match.save()
        actualiser_paris(match)


def actualiser_paris(match):
    """Actualise les paris concernant le match en question

    :param Match match: match qui necessite d'actualiser les paris
    :rtype: None
    """
    for paris in Paris.select():
        if paris.match == match:
            if (
                    paris.vainqueur == 1 and match.resultat_equipe1 > match.resultat_equipe2
            ) or (
                    paris.vainqueur == 2 and match.resultat_equipe2 > match.resultat_equipe1
            ):
                joueur = paris.joueur
                joueur.total_point += cfg.pts_paris_gagnant
                joueur.save()
            if paris.bonus_offensif and match.bonus_offensif:
                joueur = paris.joueur
                joueur.total_point += cfg.pts_bonus_offensif
                joueur.save()
            if paris.bonus_defensif and match.bonus_defensif:
                joueur = paris.joueur
                joueur.total_point += cfg.pts_bonus_defensif
                joueur.save()
            paris.delete_instance()
