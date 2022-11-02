from datetime import datetime

from telegram import InlineKeyboardButton

from src.api.Match_BDD import Match
from src.api.Paris_BDD import Paris


def liste_all_next_match():
    """liste_match: renvoi un dictionnaire des prochain match

    :return: liste dont la clef est le match_id, et la valeur le string du match
    :rtype: dict
    """
    return liste_next_match(None, True, False)


def liste_next_match_pariable(joueur):
    """liste_match: renvoi un dictionnaire des prochain match

    :param Joueur joueur: joueur sur lequel il faut filtré
    :return: liste dont la clef est le match_id, et la valeur le string du match
    :rtype: dict
    """
    return liste_next_match(joueur, False, True)


def liste_next_match_with_paris(joueur):
    """liste_match: renvoi un dictionnaire des prochain match

    :param Joueur joueur: joueur sur lequel il faut filtré
    :return: liste dont la clef est le match_id, et la valeur le string du match
    :rtype: dict
    """
    return liste_next_match(joueur, False, False)


def liste_next_match(joueur, all_match, pariable):
    """liste_match: renvoi un dictionnaire des prochain match. Possible de filtrer sur les matchs pariables

    :param bool pariable: True si on veut que les matchs pariables pour un joueur, false sinon
    :param bool all_match: True si on veut tous les match
    :param Joueur joueur: joueur sur lequel il faut filtré
    :return: liste dont la clef est le match_id, et la valeur le string du match
    :rtype: dict
    """
    reponse = {}
    for match in Match.select().where(Match.date_match > datetime.now()):
        if all_match:
            reponse[match.get_id()] = str(match)
        else:
            is_paris_existe = any(pari.match == match for pari in Paris.select().where(Paris.joueur == joueur))

            if pariable and not is_paris_existe or not pariable and is_paris_existe:
                reponse[match.get_id()] = str(match)
    return reponse


def creer_button_liste_next_match(patern):
    """creer_button_liste_next_match:

    :param string patern: partern pour le bouton
    :return: retourne la liste des prochains match.
    :rtype: list
    """
    return [InlineKeyboardButton(valeur, callback_data=f"{patern}_{key}") for key, valeur in
            liste_all_next_match().items()]


def creer_button_liste_next_match_pariable(patern, joueur):
    """Creer une liste de bouton avec les match sur lesquels il est possible de parrier

    :param string patern: partern pour le bouton
    :param Joueur joueur: joueur sur lequel on filtre les paris possible
    :return: retourne la liste des prochains match pariable
    :rtype: list
    """
    return [InlineKeyboardButton(valeur, callback_data=f"{patern}_{key}") for key, valeur in
            liste_next_match_pariable(joueur).items()]


def creer_button_liste_next_match_with_paris(patern, joueur):
    """Creer une liste de bouton avec les match sur lesquels il y a deja un paris

    :param string patern: partern pour le bouton
    :param Joueur joueur: joueur sur lequel on filtre les paris
    :return: retourne la liste des prochains match avec un paris
    :rtype: list
    """
    return [InlineKeyboardButton(valeur, callback_data=f"{patern}_{key}") for key, valeur in
            liste_next_match_with_paris(joueur).items()]
