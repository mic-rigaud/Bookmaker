#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19/12/2021 17:06
# @Author  : Michael
# @File    : paris.py
# @Project: Bookmaker

"""Permet de gerer les paris."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler)

from src.api.Joueur_BDD import get_joueur
from src.api.Restricted import restricted
from src.api.button import build_menu
from src.api.telegram_decorateur import bot_edit_message, bot_send_message
import src.plugins.paris.paris_conv_add as conv_add
import src.plugins.paris.paris_conv_modif as conv_modif
from src.plugins.paris.paris_tool import liste_paris


def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    etat = query.data.split("_")[2]
    futur = etat == "f"
    joueur = get_joueur(query.message.chat_id, query.from_user.id)
    if joueur is None:
        reponse = "Erreur, le joueur n'existe pas"
    else:
        reponse = liste_paris(joueur, futur)
    bot_edit_message(context=context, update=update, text=reponse, reply_markup=reply_markup)


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Ajouter un paris", callback_data="paris_add"),
        InlineKeyboardButton("Lister vos futurs paris", callback_data="paris_liste_f"),
        InlineKeyboardButton("Lister vos précédents paris", callback_data="paris_liste_p"),
        InlineKeyboardButton("Modifier un paris", callback_data="paris_modif"),
        ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


@restricted
def paris(update: Update, context: CallbackContext):
    """Renvoi le compte à rebour."""
    reponse = "Que souhaitez-vous faire ?\n"
    reply_markup = creer_bouton()
    bot_send_message(context=context, update=update, text=reponse, reply_markup=reply_markup, )


def add(dispatcher):
    """
    Renvoi de quoi gérer les paris.
    """
    dispatcher.add_handler(CommandHandler("paris", paris))
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^paris_liste."))
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
            conversation_timeout=30
            )
    dispatcher.add_handler(new_alarm_handler)
    new_alarm_handler2 = ConversationHandler(
            entry_points=[CallbackQueryHandler(conv_modif.button_modif, pattern="^paris_modif$")],
            states={
                conv_modif.ETAPE1: [
                    CallbackQueryHandler(conv_modif.etape1, pattern="^paris_modif1_.")
                    ],
                conv_modif.ETAPE2: [
                    CallbackQueryHandler(conv_modif.etape2, pattern="^paris_modif2_.")
                    ],
                conv_modif.ETAPE3: [
                    CallbackQueryHandler(conv_modif.etape3, pattern="^paris_modif3_.")
                    ],
                conv_modif.ETAPE4: [
                    CallbackQueryHandler(conv_modif.etape4, pattern="^paris_modif4_.")
                    ],
                },
            fallbacks=[CommandHandler("end", conv_modif.conv_cancel)],
            conversation_timeout=30
            )
    dispatcher.add_handler(new_alarm_handler2)
