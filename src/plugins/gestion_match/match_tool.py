import json
from _datetime import datetime

import requests

import config as cfg
from src.api.Match_BDD import Match
from src.api.Saisons_BDD import Saisons


## Pour les tests :
# https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:82574/lineups.json?api_key=


def get_matchs(saison_id):
    """get_matchs:"""
    url = "https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:{}/lineups.json?api_key={}".format(
        saison_id, cfg.rygby_api_key
    )
    req = requests.get(url)
    return json.loads(req.content.decode("utf-8"))["lineups"]


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
