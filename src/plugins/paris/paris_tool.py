#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 22/12/2021 17:32
# @Author  : Michael
# @File    : paris_tool.py
# @Project: Bookmaker


from src.api.Paris_BDD import Paris


def liste_paris(joueur):
    reponse = "Voici la liste de vos paris:\n"
    paris = Paris.select().where(Paris.joueur == joueur).order_by(Paris.date_match)
    for pari in paris:
        reponse += "\n" + pari.afficher_paris()
    return reponse
