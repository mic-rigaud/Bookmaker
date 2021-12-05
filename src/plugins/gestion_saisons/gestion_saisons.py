"""Renvoi la liste des utilisateurs actuels."""
import logging

from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

from src.api.Restricted import restricted_admin
from src.api.Saisons_BDD import Saisons
from src.api.button import build_menu
from src.plugins.gestion_saisons.saison_tool import (
    lister_saison,
    ajouter_saison,
    supprimer_saison,
)


def get_liste_saison():
    record = Saisons.select().where(True)
    return {saison.id: saison.nom for saison in record}


def button_add(update: Update, context: CallbackContext):
    query = update.callback_query
    if "gsaison" in query.data:
        reponse = "Voici la liste des saisons que vous pouvez ajouter"
        reply_markup = creer_bouton_liste(lister_saison(), "add")
    else:
        saison_id = query.data.split("_")[2]
        reponse = ajouter_saison(saison_id)
        reply_markup = query.message.reply_markup
    # Evite l'erreur du message égal au précédent
    if reponse == query.message.text:
        reponse += "."
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_supp(update: Update, context: CallbackContext):
    query = update.callback_query
    if "gsaison" in query.data:
        reponse = "Quelle saison souhaitez vous supprimer ?"
    else:
        saison_id = query.data.split("_")[2]
        reponse = supprimer_saison(saison_id)
    reply_markup = creer_bouton_liste(get_liste_saison(), "supp")
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def creer_bouton_liste(liste_saisons, fonction):
    try:
        button_list = []
        for saison_id in liste_saisons:
            line = str(liste_saisons[saison_id])
            button_list.append(
                InlineKeyboardButton(
                    line, callback_data="gs_{}_{}".format(fonction, str(saison_id))
                )
            )
        # button_list.append(InlineKeyboardButton("Retour", callback_data="gsaison_home"))
        return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    except Exception:
        logging.warning("<i>Aucune saisons dans la liste</i>")


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Ajouter saison", callback_data="gsaison_add"),
        InlineKeyboardButton("Supprimer saison", callback_data="gsaison_supp"),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


@restricted_admin
def gestion_saison(update: Update, context: CallbackContext):
    """Renvoi le compte à rebour."""
    reponse = "Voici la liste des saisons suivies par le bot:\n"
    liste_saison = get_liste_saison()
    for key in liste_saison:
        reponse += "{}\n".format(liste_saison[key])
    reply_markup = creer_bouton()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """
    Renvoi de quoi gérer les saisons suivies.
    """
    dispatcher.add_handler(CommandHandler("gestion_saisons", gestion_saison))
    dispatcher.add_handler(CallbackQueryHandler(button_add, pattern="^gsaison_add$"))
    dispatcher.add_handler(CallbackQueryHandler(button_supp, pattern="^gsaison_supp$"))
    dispatcher.add_handler(CallbackQueryHandler(button_add, pattern="^gs_add_."))
    dispatcher.add_handler(CallbackQueryHandler(button_supp, pattern="^gs_supp_."))
