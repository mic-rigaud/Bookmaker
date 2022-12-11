import logging

from telegram import MAX_MESSAGE_LENGTH, ParseMode


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


class TelegramCallbackError(Exception):
    def __init__(self, message=""):
        self.message = message
