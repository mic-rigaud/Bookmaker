"""Ajoute les utilisateurs"""

import logging

from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

import config as cfg
from src.api.Joueur_BDD import Joueur

ETAPE1, ETAPE2 = range(2)


def bonjour(update: Update, context: CallbackContext):
    """Gere les bonjour."""
    record = Joueur.select().where(Joueur.chat_id == update.message.chat_id)
    if not record.exists():
        reponse = "Bonjour!\nJe suis un Bookmaker spécialisé dans le rugby! Je vais te permettre de faire quelques petits paris entre copains. Avant de commencer à prendre tes paris, pourrais tu me donner le mot de passe ?"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
        )
        return ETAPE1
    else:
        reponse = "Mais on se connait déjà tous les deux.😉\nFais /help si tu veux connaitre mes capacités."
        context.bot.send_message(
            chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
        )
        return ConversationHandler.END


def etape1(update: Update, context: CallbackContext):
    mdp = update.message.text
    if mdp.lower() == cfg.mdp:
        reponse = "Super! Tu fais bien parti du groupe! Comment tu t'appelles?"
        context.bot.send_message(
            chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
        )
        return ETAPE2
    else:
        reponse = "Désolé! Ce n'est pas le bon mot de passe. Au revoir."
        context.bot.send_message(
            chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
        )
        return ConversationHandler.END


def etape2(update: Update, context: CallbackContext):
    nom = update.message.text
    chat_id = update.message.chat_id
    Joueur.create(nom=nom, chat_id=chat_id).save()
    logging.info("Ajout de l'utilisateur {}".format(nom))
    reponse = "Bienvenue à toi {}.\nMaintenant à toi de jouer! Les paris sont ouverts!\n Au fait, si tu as besoin d'en savoir plus sur mes fonctionnalités fais /help".format(
        nom
    )
    context.bot.send_message(
        chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def conv_cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Bon c'est fini")
    return ConversationHandler.END


def add(dispatcher):
    """
    Ajoute les utilisateurs
    """
    new_alarm_handler = ConversationHandler(
        entry_points=[CommandHandler("bonjour", bonjour)],
        states={
            ETAPE1: [MessageHandler(Filters.text, etape1)],
            ETAPE2: [MessageHandler(Filters.text, etape2)],
        },
        fallbacks=[CommandHandler("end", conv_cancel)],
    )
    dispatcher.add_handler(new_alarm_handler)
