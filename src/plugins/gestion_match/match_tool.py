import json
import logging
from _datetime import datetime

import pytz
import requests

import config as cfg
from src.api.Match_BDD import Match
from src.api.Paris_BDD import Paris
from src.api.Saisons_BDD import Saisons


## Pour les tests :
# https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:82574/lineups.json?api_key=


def get_matchs(saison_id):
    """get_matchs:"""
    url = "https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:{}/lineups.json?api_key={}".format(
        saison_id, cfg.rygby_api_key
    )
    req = requests.get(url)
    try:
        return json.loads(req.content.decode("utf-8"))["lineups"]
    except Exception as e:
        logging.warning("Erreur avec {}\n retour : {}\n{}".format(url, req, str(e)))
        return None


def get_info_matchs(match_id):
    """get_matchs:"""

    url = "https://api.sportradar.us/rugby-union/trial/v3/fr/sport_events/sr:match:{}/summary.json?api_key={}".format(
        match_id, cfg.rygby_api_key
    )
    req = requests.get(url)
    try:
        return json.loads(req.content.decode("utf-8"))
    except Exception as e:
        logging.warning("Erreur avec {}\n retour : {}\n{}".format(url, req, str(e)))
        return None


def add_match_bdd(match):
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
    """add_match_bdd:"""
    for saison in Saisons.select():
        matchs = get_matchs(saison.season_id)
        for match in matchs:
            add_match_bdd(match)
    return "Matchs ajouté avec succès"


def liste_match():
    """liste_match:"""
    reponse = "Voici les matchs disponibles:\n"
    for match in Match.select():
        reponse += "{} - {}\n".format(match.equipe1, match.equipe2)
    return reponse


def refresh_match():
    for match in Match.select():
        if match.get_date_match() <= datetime.now().replace(tzinfo=pytz.UTC):
            actualiser_match(match)
    return "Resultat bien mis à jour"


def actualiser_match(match):
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
