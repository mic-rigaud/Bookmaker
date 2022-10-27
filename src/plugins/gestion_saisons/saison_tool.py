from datetime import datetime
import json
import logging

from peewee import DoesNotExist
import requests

import config as cfg
from src.api.Match_BDD import Match
from src.api.Saisons_BDD import Saisons


def get_seasons():
    """get_seasons:"""
    url = (
            "https://api.sportradar.us/rugby-union/trial/v3/fr/seasons.json?api_key="
            + cfg.rugby_api_key
    )
    req = requests.get(url)
    return json.loads(req.content.decode("utf-8"))["seasons"]


def lister_saison():
    """recherche_saison:"""
    # pour lister les saison : https://api.sportradar.us/rugby-union/trial/v3/fr/seasons.xml?api_key= pour obtenir
    # les matches de la saison : https://api.sportradar.us/rugby-union/trial/v3/fr/seasons/sr:season:82574/lineups
    # .xml?api_key=
    liste_saisons = {}
    saisons = get_seasons()
    for saison in saisons:
        date_fin_saison = datetime.strptime(saison["end_date"], "%Y-%m-%d")
        if date_fin_saison > datetime.now():
            liste_saisons[saison["id"].split(":")[2]] = saison["name"]
    return liste_saisons


def is_present(saison_id):
    saison = Saisons.select().where(Saisons.season_id == saison_id).count()
    return saison > 0


def ajouter_saison(saison_id):
    if is_present(saison_id):
        return "Cette saison est déjà présente"
    liste_saison = get_seasons()
    for saison in liste_saison:
        if str(saison_id) in saison["id"]:
            saison_ajout = Saisons()
            saison_ajout.season_id = saison_id
            saison_ajout.expiration = datetime.strptime(saison["end_date"], "%Y-%m-%d")
            saison_ajout.nom = saison["name"]
            saison_ajout.save()
            logging.info(f'La saison {saison["name"]} a bien été ajouté')
            return f'la saison {saison["name"]} a bien été ajouté'
    logging.warning("Erreur lors de l'ajout de la saison")
    return "Erreur lors de l'enregistrement de la saison"


def supprimer_saison(saison_id):
    """supprimer_saison:"""
    try:
        saison = Saisons.get_by_id(saison_id)
        logging.info(f"Suppression de la saison {saison.nom}")
        for match in Match.select().where(Match.saison == saison):
            nb_delete = match.delete_instance()
            if nb_delete != 1:
                logging.error(f"Erreur trop d'élément supprimer dans la BDD Match: {nb_delete}")
        nb_delete = saison.delete_instance()
        if nb_delete != 1:
            logging.error(f"Erreur trop d'élément supprimer dans la BDD Saison: {nb_delete}")
        return f"Suppression avec succes de la saison {saison.nom}"
    except DoesNotExist as e:
        logging.info("La saison demandé n'existe pas")
        return "Erreur la saison n'existe pas"
