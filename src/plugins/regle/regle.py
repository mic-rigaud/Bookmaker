#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 29/10/2022 18:12
# @Author  : Michael
# @File    : regle.py.py
# @Project: Bookmaker

"""Affiche les règles du jeu"""

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

import config as cfg
from src.api.Restricted import restricted
from src.api.telegram_decorateur import bot_send_message


def get_regle():
    """get_regle: renvoi les regle

    :rtype: str"""
    return f"<b>Voici les règles du Jeu</b> \n\nVous pouvez faire des paris sur des matchs.\nDans ce jeu, le point de " \
           f"bonus offensif est compté que pour l'équipe vainqueur. Il est compté comme acquis si l'équipe réalise au " \
           f"moins 4 essais. Le point de bonus défensif est acquis si l'équipe perdante perd avec moins de 7 points. " \
           f"\n\n<i>Les joueurs gagnent les points suivants:</i>\nVictoire de la bonne équipe : {cfg.pts_paris_gagnant}" \
           f"\nPoint de bonus offensif gagné par le vainqueur: {cfg.pts_bonus_offensif}\nPoint de bonus defensif gagné " \
           f"par le perdant: {cfg.pts_bonus_defensif} "


@restricted
def regle(update: Update, context: CallbackContext):
    """Affiche les règles du jeu"""
    bot_send_message(update, context, text=get_regle())


def add(dispatcher):
    """
    Affiche les règles du jeu
    """
    handler = CommandHandler('regle', regle)
    dispatcher.add_handler(handler)
