"""Permet de gerer les matchs pour un admin"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from src.api.Restricted import restricted_admin
from src.api.button import bot_edit_message, bot_send_message, build_menu
from src.plugins.gestion_match.match_tool import add_match, delete_matchs, liste_match, refresh_match


@restricted_admin
def button_add(update: Update, context: CallbackContext):
    reply_markup = creer_bouton()
    bot_edit_message(update, context, "Ajout des matchs en cours", reply_markup)
    reponse = add_match()
    bot_edit_message(update, context, reponse, reply_markup)


@restricted_admin
def button_rm(update: Update, context: CallbackContext):
    reply_markup = creer_bouton()
    reponse = delete_matchs()
    bot_edit_message(update, context, reponse, reply_markup)


@restricted_admin
def button_liste(update: Update, context: CallbackContext):
    reply_markup = creer_bouton()
    reponse = liste_match()
    bot_edit_message(update, context, reponse, reply_markup)


@restricted_admin
def button_refresh(update: Update, context: CallbackContext):
    reply_markup = creer_bouton()
    bot_edit_message(update, context, "Actualisation des matchs en cours", reply_markup)
    reponse = refresh_match()
    bot_edit_message(update, context, reponse, reply_markup)


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Ajouter matchs", callback_data="gmatch_add"),
        InlineKeyboardButton("Actualiser résultats", callback_data="gmatch_refresh"),
        InlineKeyboardButton("Lister les matchs", callback_data="gmatch_liste"),
        InlineKeyboardButton("Supprimer les matchs", callback_data="gmatch_rm"),
        ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


@restricted_admin
def gestion_match(update: Update, context: CallbackContext):
    """Permet de gerer les matchs."""
    bot_send_message(context=context, update=update, text="Voici les actions sur la gestion des matchs:\n",
                     reply_markup=creer_bouton())


def add(dispatcher):
    """
    Renvoi de quoi gérer les match.
    """
    dispatcher.add_handler(CommandHandler("gestion_match", gestion_match))
    dispatcher.add_handler(CallbackQueryHandler(button_add, pattern="^gmatch_add"))
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^gmatch_liste"))
    dispatcher.add_handler(CallbackQueryHandler(button_rm, pattern="^gmatch_rm"))
    dispatcher.add_handler(
            CallbackQueryHandler(button_refresh, pattern="^gmatch_refresh")
            )
