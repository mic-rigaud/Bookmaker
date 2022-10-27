from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update)
from telegram.ext import CallbackContext, ConversationHandler

from src.api.Gestion_Match import creer_button_liste_next_match_pariable
from src.api.Joueur_BDD import get_joueur
from src.api.Match_BDD import Match
from src.api.Paris_BDD import Paris
from src.api.button import build_menu


ETAPE1, ETAPE2, ETAPE3, ETAPE4 = range(4)


def button_add(update: Update, context: CallbackContext):
    # Traitement réponse
    query = update.callback_query
    joueur = get_joueur(query.message.chat_id, query.from_user.id)
    if joueur is None:
        context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Le joueur n'existe pas",
                parse_mode=ParseMode.HTML,
                )
        return ConversationHandler.END
    paris = Paris(joueur=joueur)
    context.user_data[0] = paris
    # Traitement question
    reponse = "Sur quel match souhaitez vous faire un paris?"
    reply_markup = InlineKeyboardMarkup(
            build_menu(creer_button_liste_next_match_pariable("paris_add1", joueur), n_cols=1)
            )
    context.bot.edit_message_text(
            message_id=query.message.message_id,
            chat_id=query.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )
    return ETAPE1


def etape1(update: Update, context: CallbackContext):
    # Traitement réponse
    paris = context.user_data[0]
    query = update.callback_query
    match_id = query.data.split("_")[2]
    paris.match = Match.get_by_id(match_id)
    paris.date_match = paris.match.get_date_match()
    # Traitement question
    reponse = "Quel équipe sera vainqueur ?"
    button_list = [
        InlineKeyboardButton(paris.match.equipe1, callback_data="paris_add2_1"),
        InlineKeyboardButton(paris.match.equipe2, callback_data="paris_add2_2"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.edit_message_text(
            message_id=query.message.message_id,
            chat_id=query.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )
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
        InlineKeyboardButton("oui", callback_data="paris_add3_1"),
        InlineKeyboardButton("non", callback_data="paris_add3_2"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.edit_message_text(
            message_id=query.message.message_id,
            chat_id=query.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )
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
        InlineKeyboardButton("oui", callback_data="paris_add4_1"),
        InlineKeyboardButton("non", callback_data="paris_add4_2"),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.edit_message_text(
            message_id=query.message.message_id,
            chat_id=query.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )
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
    context.bot.edit_message_text(
            message_id=query.message.message_id,
            chat_id=query.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            reply_markup=None,
            )
    return ConversationHandler.END


def conv_cancel(update: Update, context: CallbackContext):
    reponse = "Au revoir"
    context.bot.send_message(
            chat_id=update.message.chat_id,
            text=reponse,
            parse_mode=ParseMode.HTML,
            )
    return ConversationHandler.END
