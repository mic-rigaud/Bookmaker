"""Creer le decorateur restricted."""
from functools import wraps
import logging

from telegram import ParseMode, Update
from telegram.ext import CallbackContext

import config as cfg
from src.api.Joueur_BDD import Joueur


def restricted(func):
    """Rends les commandes en restricted."""

    @wraps(func)
    def wrapped(update: Update, context: CallbackContext):
        message = update.callback_query if update.message is None else update.message
        user_id = message.from_user.id
        record = Joueur.select().where(Joueur.user_id == user_id)
        if not record.exists():
            logging.info("Access non autorisé pour {}.".format(user_id))
            reponse = (
                "Hey! Mais on se connait pas tout les deux.\nTa maman ne t'as jamais dit qu'on commence "
                "toujours une conversation par /bonjour. "
            )
            context.bot.send_message(
                    chat_id=message.chat_id, text=reponse, parse_mode=ParseMode.HTML
                    )
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
            logging.info(
                    "Access non autorisé pour {} sur une fonction d'admin.".format(user_id)
                    )
            reponse = "C'est une fonction d'admin. C'est pas pour toi, désolé."
            context.bot.send_message(
                    chat_id=message.chat_id, text=reponse, parse_mode=ParseMode.HTML
                    )
            return
        return func(update, context)

    return wrapped
