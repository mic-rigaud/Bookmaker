#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/12/2021 10:39
# @Author  : Michael
# @File    : classement.py
# @Project: Bookmaker

"""Permet d'avoir le classement des joueurs"""

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from src.api.Joueur_BDD import Joueur
from src.api.Restricted import restricted
from src.api.button import bot_send_message


def get_classement_users_in_chat(chat_id):
    record = Joueur.select().where(Joueur.chat_id == chat_id).order_by(Joueur.total_point.desc())

    reponse = "Voici la liste des joueurs:\n"
    for i, person in enumerate(record, start=1):
        reponse += f"{str(i)}: {person.nom} ({str(person.total_point)} pts)\n"
    return reponse


def get_classement_users_alone():
    record = Joueur.select().where(Joueur.chat_id == Joueur.user_id).order_by(Joueur.total_point.desc())

    reponse = "Voici la liste des joueurs:\n"
    for i, person in enumerate(record, start=1):
        reponse += f"{str(i)}: {person.nom} ({str(person.total_point)} pts)\n"
    return reponse


@restricted
def classement(update: Update, context: CallbackContext):
    """Renvoi le classement des joueurs."""
    if update.message.chat_id == update.message.from_user.id:
        reponse = get_classement_users_alone()
    else:
        reponse = get_classement_users_in_chat(update.message.chat_id)
    bot_send_message(update, context, text=reponse)


def add(dispatcher):
    """
    Renvoi le classement des joueurs.
    """
    dispatcher.add_handler(CommandHandler("classement", classement))
