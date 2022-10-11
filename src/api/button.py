import json
import logging

import telegram
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from src.api.Restricted import restricted


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """Permet de construire un menu interactif."""
    menu = [buttons[i: i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


@restricted
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    try:
        data = json.loads(query.data)
    except json.JSONDecodeError:
        data = query.data

    module_name = data["module"]
    mod = __import__(f"actions.{module_name}", fromlist=[""])
    reponse, reply_markup = mod.button(update, context)

    try:
        context.bot.edit_message_text(
                text=reponse,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode=telegram.ParseMode.HTML,
                reply_markup=reply_markup,
                )
    except BadRequest as ex:
        logging.error("Error: meme message et meme reply_markup\n" + str(ex))


def build_callback(data):
    return_value = json.dumps(data)
    if len(return_value) > 64:
        raise TelegramCallbackError("Les data ont une taille supérieur à 64 bytes")
    return return_value


class TelegramCallbackError(Exception):
    def __init__(self, message=""):
        self.message = message


def bot_send_message(update, context, text, reply_markup=None, chat_id=None):
    """Envoi un message

    :param int chat_id: Chat id si on veut en specifier un
    :param Update or None update: update du bot
    :param CallbackContext context: context du bot
    :param str text: text a envoyer
    :param ReplyMarkup reply_markup: reply_markup
    """
    if len(text) > MAX_MESSAGE_LENGTH - 1:
        text = text[:MAX_MESSAGE_LENGTH - 1]
        logging.warning("Tentative d'envoyer un texte trop long. Il a été réduit à la taille maximale possible.")
    if update is None and chat_id is None:
        logging.error("Il manque un argument")
    elif update is not None:
        query = update if update.callback_query is None else update.callback_query
        if text == query.message.text:
            text += "."
        if not chat_id:
            chat_id = query.message.chat_id
    context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )


def bot_edit_message(update, context, text, reply_markup=None, message_id=None):
    """Edit le dernier message

    :param int message_id: id du message a modifier sinon prend le dernier
    :param Update update: update du bot
    :param CallbackContext context: context du bot
    :param str text: text a envoyer
    :param ReplyMarkup reply_markup: reply_markup"""

    query = update if update.callback_query is None else update.callback_query
    message_id = query.message.message_id if message_id is None else message_id
    if len(text) > MAX_MESSAGE_LENGTH - 1:
        text = text[:MAX_MESSAGE_LENGTH - 1]
        logging.warning("Tentative d'envoyer un texte trop long. Il a été réduit à la taille maximale possible.")
    if text == query.message.text:
        text += "."
    context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            )
