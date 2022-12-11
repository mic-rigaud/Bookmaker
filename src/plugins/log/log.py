# @Author: michael
# @Date:   11-Aug-2018
# @Filename: log.py
# @Last modified by:   michael
# @Last modified time: 08-Nov-2019
# @License: GNU GPL v3

"""Gere les logs."""

import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

import config as cfg
from src.api.Restricted import restricted_admin
from src.api.telegram_decorateur import bot_send_message


def log_status():
    """Affiche les 10 dernieres lignes."""
    reponse = ""
    with open(cfg.log, "r") as f:
        for ligne in f.readlines()[-10:]:
            reponse += ligne.replace("<", "").replace("module", "main").replace(">", "")
    return reponse


def log_rm():
    """Supprime les log."""
    with open(cfg.log, "w") as f:
        f.write("")
    logging.info("Fichier de log supprimé")


@restricted_admin
def log(update: Update, context: CallbackContext):
    """Gere les log."""
    demande = " ".join(context.args).lower().split(" ")[0]
    if demande in ["ls", ""]:
        reponse = "<b>Voici les 10 derniers log:</b>\n"
        reponse += log_status()
    elif demande == "rm":
        reponse = "<b>Suppression des log.</b>"
        log_rm()
    else:
        reponse = "<b>Commande inexistante. Taper /help log</b>"
    bot_send_message(update=update, context=context, text=reponse)


def add(dispatcher):
    """
    Gere les log.

    ls - affiche les 10 dernieres lignes
    rm - supprime les log
    """
    handler = CommandHandler("log", log, pass_args=True)
    dispatcher.add_handler(handler)
