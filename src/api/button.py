import json
import logging

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from src.api.Restricted import restricted
from src.api.telegram_decorateur import TelegramCallbackError, bot_edit_message


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

    # noinspection PyTypeChecker
    module_name = data["module"]
    mod = __import__(f"actions.{module_name}", fromlist=[""])
    reponse, reply_markup = mod.button(update, context)

    try:
        bot_edit_message(update, context, text=reponse, reply_markup=reply_markup)
    except BadRequest as ex:
        logging.error("Error: meme message et meme reply_markup\n" + str(ex))


def build_callback(data):
    return_value = json.dumps(data)
    if len(return_value) > 64:
        raise TelegramCallbackError("Les data ont une taille supérieur à 64 bytes")
    return return_value
