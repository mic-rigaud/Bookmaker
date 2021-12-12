#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/12/2021 10:39
# @Author  : Michael
# @File    : classement.py
# @Project: Bookmaker

"""Permet d'avoir le classement des joueurs"""

from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext

from src.api.Joueur_BDD import Joueur
from src.api.Restricted import restricted


def get_classement_user(chat_id):
    record = (
        Joueur.select()
            .where(Joueur.chat_id == chat_id)
            .order_by(Joueur.total_point.desc())
    )
    reponse = "Voici la liste des joueurs:\n"
    for i, person in enumerate(record, start=1):
        reponse += "{}: {} ({} pts)\n".format(
            str(i), person.nom, str(person.total_point)
        )
    return reponse


@restricted
def classement(update: Update, context: CallbackContext):
    """Renvoi le classement des joueurs."""
    reponse = get_classement_user(update.message.chat_id)
    context.bot.send_message(
        chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
    )


def add(dispatcher):
    """
    Renvoi le classement des joueurs.
    """
    dispatcher.add_handler(CommandHandler("classement", classement))
