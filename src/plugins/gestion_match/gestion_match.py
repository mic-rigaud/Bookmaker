"""Permet de gerer les matchs pour un admin"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from src.api.Restricted import restricted_admin
from src.api.button import bot_edit_message, build_menu
from src.plugins.gestion_match.match_tool import add_match, delete_matchs, liste_match, refresh_match


@restricted_admin
def button_add(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = add_match()
    # Evite l'erreur du message égal au précédent
    if reponse == query.message.text:
        reponse += "."
    bot_edit_message(update, context, reponse, reply_markup)


@restricted_admin
def button_rm(update: Update, context: CallbackContext):
    reply_markup = creer_bouton()
    reponse = delete_matchs()
    bot_edit_message(update, context, reponse, reply_markup)


@restricted_admin
def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = liste_match()
    # Evite l'erreur du message égal au précédent
    if reponse == query.message.text:
        reponse += "."
    bot_edit_message(update, context, reponse, reply_markup)


@restricted_admin
def button_refresh(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = refresh_match()
    # Evite l'erreur du message égal au précédent
    if reponse == query.message.text:
        reponse += "."
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
    reponse = "Voici les actions sur la gestion des matchs:\n"
    reply_markup = creer_bouton()
    context.bot.send_message(
            chat_id=update.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )


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
