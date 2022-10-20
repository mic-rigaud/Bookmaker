#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 22/12/2021 17:32
# @Author  : Michael
# @File    : paris_tool.py
# @Project: Bookmaker

from datetime import datetime

from src.api.Paris_BDD import Paris


def liste_paris(joueur, passer=False):
    reponse = "Voici la liste de vos paris:\n"
    if passer:
        paris = Paris.select().where(Paris.joueur == joueur and Paris.date_match > datetime.now()).order_by(
                Paris.date_match)
    else:
        paris = Paris.select().where(Paris.joueur == joueur and Paris.date_match <= datetime.now()).order_by(
                Paris.date_match)
    for pari in paris:
        reponse += "\n" + pari.afficher_paris()
    return reponse
