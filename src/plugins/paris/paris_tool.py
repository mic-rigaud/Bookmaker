#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 22/12/2021 17:32
# @Author  : Michael
# @File    : paris_tool.py
# @Project: Bookmaker

from datetime import datetime

from src.api.Paris_BDD import Paris


def liste_paris(joueur, passer=False):
    reponse = "Voici la liste de vos paris:"
    if passer:
        paris = Paris.select().where((Paris.joueur == joueur) & (Paris.date_match > datetime.now())).order_by(
                Paris.date_match)
    else:
        paris = Paris.select().where((Paris.joueur == joueur) & (Paris.date_match <= datetime.now())).order_by(
                Paris.date_match.desc())
    for pari in paris[:7]:
        reponse += "\n\n" + pari.afficher_paris()
    if len(paris) > 7:
        reponse += f"\n\n<i>Seul les 7 {'prochains' if passer else 'précédents'} paris sont affichés par manque de " \
                   f"place</i> "
    return reponse
