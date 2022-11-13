"""Creer le decorateur restricted."""
from functools import wraps
import logging

from telegram import Update
from telegram.ext import CallbackContext

import config as cfg
from src.api.Joueur_BDD import Joueur
from src.api.button import bot_send_message


def restricted(func):
    """Rends les commandes en restricted."""

    @wraps(func)
    def wrapped(update: Update, context: CallbackContext):
        message = update.callback_query if update.message is None else update.message
        user_id = message.from_user.id
        record = Joueur.select().where(Joueur.user_id == user_id)
        if not record.exists():
            logging.info(f"Access non autorisé pour {user_id}.")
            reponse = ("Hey! Mais on se connait pas tout les deux.\nTa maman ne t'as jamais dit qu'on commence "
                       "toujours une conversation par /bonjour. ")
            bot_send_message(context=context, update=update, text=reponse)
            return
        return func(update, context)

    return wrapped


def restricted_admin(func):
    """Rends les commandes en restricted."""

    @wraps(func)
    def wrapped(update: Update, context: CallbackContext):
        message = update.callback_query if update.message is None else update.message
        user_id = message.from_user.id
        if user_id not in cfg.admin_chatid:
            logging.info(f"Access non autorisé pour {user_id} sur une fonction d'admin.")
            reponse = "C'est une fonction d'admin. C'est pas pour toi, désolé."
            bot_send_message(context=context, update=update, text=reponse)
            return
        return func(update, context)

    return wrapped
