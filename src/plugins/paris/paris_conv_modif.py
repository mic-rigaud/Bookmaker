from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram.ext import CallbackContext, ConversationHandler

from src.api.Gestion_Match import creer_button_liste_next_match_with_paris
from src.api.Joueur_BDD import get_joueur
from src.api.Match_BDD import Match
from src.api.Paris_BDD import get_paris
from src.api.button import bot_edit_message, bot_send_message, build_menu


ETAPE1, ETAPE2, ETAPE3, ETAPE4 = range(4)


def button_modif(update: Update, context: CallbackContext):
    # Traitement réponse
    query = update.callback_query
    joueur = get_joueur(query.message.chat_id, query.from_user.id)
    if joueur is None:
        bot_edit_message(update=update, context=context, text="Le joueur n'existe pas")
        return ConversationHandler.END
    context.user_data[0] = joueur
    # Traitement question
    reponse = "Quel paris souhaitez-vous modifier ?"
    reply_markup = InlineKeyboardMarkup(
            build_menu(creer_button_liste_next_match_with_paris("paris_modif1", joueur), n_cols=1)
            )
    bot_edit_message(update=update, context=context, text=reponse, reply_markup=reply_markup)
    return ETAPE1


def etape1(update: Update, context: CallbackContext):
    # Traitement réponse
    joueur = context.user_data[0]
    query = update.callback_query
    match_id = query.data.split("_")[2]
    match = Match.get_by_id(match_id)
    paris = get_paris(joueur, match)
    context.user_data[0] = paris
    # Traitement question
    bot_edit_message(update=update, context=context,
                     text=f"Vous avez choisi de modifier le paris de ce match:\n {match}")

    reponse = "Quel équipe sera vainqueur ?"
    button_list = [
        InlineKeyboardButton(paris.match.equipe1, callback_data="paris_modif2_1"),
        InlineKeyboardButton(paris.match.equipe2, callback_data="paris_modif2_2"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot_send_message(update=update, context=context, text=reponse, reply_markup=reply_markup)
    return ETAPE2


def etape2(update: Update, context: CallbackContext):
    # Traitement réponse

    query = update.callback_query
    paris = context.user_data[0]
    paris.vainqueur = query.data.split("_")[2]
    context.user_data[0] = paris
    # Traitement question
    reponse = "Avec un point de bonus offensif ?"
    button_list = [
        InlineKeyboardButton("oui", callback_data="paris_modif3_1"),
        InlineKeyboardButton("non", callback_data="paris_modif3_2"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot_edit_message(update=update, context=context, text=reponse, reply_markup=reply_markup)
    return ETAPE3


def etape3(update: Update, context: CallbackContext):
    # Traitement réponse
    query = update.callback_query
    ptoffensif = query.data.split("_")[2]
    paris = context.user_data[0]
    paris.bonus_offensif = ptoffensif == "1"
    context.user_data[0] = paris
    # Traitement question
    reponse = "Avec un point de bonus défensif ?"
    button_list = [
        InlineKeyboardButton("oui", callback_data="paris_modif4_1"),
        InlineKeyboardButton("non", callback_data="paris_modif4_2"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot_edit_message(update=update, context=context, text=reponse, reply_markup=reply_markup)
    return ETAPE4


def etape4(update: Update, context: CallbackContext):
    # Traitement réponse
    query = update.callback_query
    ptdefensif = query.data.split("_")[2]
    paris = context.user_data[0]
    paris.bonus_defensif = ptdefensif == "1"
    paris.save()
    # Traitement question
    reponse = "Votre paris a bien été enregistré"
    bot_edit_message(update=update, context=context, text=reponse, reply_markup=None)
    return ConversationHandler.END


def conv_cancel(update: Update, context: CallbackContext):
    bot_send_message(update=update, context=context, text="Au revoir")
    return ConversationHandler.END
