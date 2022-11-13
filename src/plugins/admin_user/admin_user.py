"""Renvoi la liste des utilisateurs actuels."""

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from src.api.Joueur_BDD import Joueur
from src.api.Restricted import restricted_admin
from src.api.button import bot_send_message


def get_liste_user():
    record = Joueur.select().where(True)
    reponse = "Voici la liste des utilisateurs:\n"
    for person in record:
        reponse += f"{person.nom}\n"
    return reponse


@restricted_admin
def admin_user(update: Update, context: CallbackContext):
    """Renvoi la liste des joueurs."""
    bot_send_message(context=context, update=update, text=get_liste_user())


def add(dispatcher):
    """
    Renvoi la liste des joueurs.
    """
    dispatcher.add_handler(CommandHandler("admin_user", admin_user))
