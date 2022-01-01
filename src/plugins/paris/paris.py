#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19/12/2021 17:06
# @Author  : Michael
# @File    : paris.py
# @Project: Bookmaker

"""Permet de gerer les paris."""
from telegram import ParseMode, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
)

import src.plugins.paris.paris_conv_add as conv_add
from src.api.Joueur_BDD import get_joueur
from src.api.Restricted import restricted
from src.api.button import build_menu
from src.plugins.paris.paris_tool import liste_paris


def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    joueur = get_joueur(query.message.chat_id, query.from_user.id)
    if joueur is None:
        reponse = "Erreur, le joueur n'existe pas"
    else:
        reponse = liste_paris(joueur)
    if query.message.text[-1] != ".":
        reponse += "."
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Ajouter un paris", callback_data="paris_add"),
        InlineKeyboardButton("Lister vos paris", callback_data="paris_liste"),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


@restricted
def paris(update: Update, context: CallbackContext):
    """Renvoi le compte à rebour."""
    reponse = "Que souhaitez-vous faire ?\n"
    reply_markup = creer_bouton()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """
    Renvoi de quoi gérer les paris.
    """
    dispatcher.add_handler(CommandHandler("paris", paris))
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^paris_liste"))
    new_alarm_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(conv_add.button_add, pattern="^paris_add$")],
        states={
            conv_add.ETAPE1: [
                CallbackQueryHandler(conv_add.etape1, pattern="^paris_add1_.")
            ],
            conv_add.ETAPE2: [
                CallbackQueryHandler(conv_add.etape2, pattern="^paris_add2_.")
            ],
            conv_add.ETAPE3: [
                CallbackQueryHandler(conv_add.etape3, pattern="^paris_add3_.")
            ],
            conv_add.ETAPE4: [
                CallbackQueryHandler(conv_add.etape4, pattern="^paris_add4_.")
            ],
        },
        fallbacks=[CommandHandler("end", conv_add.conv_cancel)],
    )
    dispatcher.add_handler(new_alarm_handler)
