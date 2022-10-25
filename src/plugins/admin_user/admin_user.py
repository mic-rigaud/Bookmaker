"""Renvoi la liste des utilisateurs actuels."""

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from src.api.Joueur_BDD import Joueur
from src.api.Restricted import restricted_admin


def get_liste_user():
    record = Joueur.select().where(True)
    reponse = "Voici la liste des utilisateurs:\n"
    for person in record:
        reponse += "{}\n".format(person.nom)
    return reponse


@restricted_admin
def admin_user(update: Update, context: CallbackContext):
    """Renvoi la liste des joueurs."""
    reponse = get_liste_user()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=reponse, parse_mode=ParseMode.HTML
    )


def add(dispatcher):
    """
    Renvoi la liste des joueurs.
    """
    dispatcher.add_handler(CommandHandler("admin_user", admin_user))
