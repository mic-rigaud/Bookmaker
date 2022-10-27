import logging
import os
import sys

import telegram
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    )

import config as cfg
from src.api.Restricted import restricted


sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

logging.basicConfig(
        filename=cfg.log,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
        )

HELP_LIST = []


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)


@restricted
def unknown(update: Update, context: CallbackContext):
    """Gere la reponse pour une commande inconnue."""
    context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Désolé je n'ai pas compris.\nFais /help si tu veux savoir ce que je sais faire.",
            )


@restricted
def help(update: Update, context: CallbackContext):
    """Affiche l'aide."""
    demande = " ".join(context.args).lower().split(" ")[0]
    reponse = "Voici les actions possibles:\n\n"
    for mod in HELP_LIST:
        doc = mod.__doc__
        nom = mod.__name__.replace("src.plugins.", "").split(".")[0]
        if doc and (
                (
                        update.message.from_user.id not in cfg.admin_chatid
                        and nom
                        not in ["bonjour", "admin_user", "gestion_saisons", "gestion_match"]
                )
                or update.message.from_user.id in cfg.admin_chatid
        ):
            if demande == "":
                reponse += f"/{nom} : {doc}" + "\n"
            elif demande in nom:
                reponse = mod.add.__doc__

    context.bot.send_message(
            chat_id=update.message.chat_id, text=reponse, parse_mode=telegram.ParseMode.HTML
            )


def charge_plugins(main_dispatcher):
    """Charge l'ensemble des plugins."""
    lst_import = os.listdir("./src/plugins")
    for module_name in lst_import:
        if "__" not in module_name:
            mod = __import__(f"src.plugins.{module_name}.{module_name}", fromlist=[""])
            mod.add(main_dispatcher)
            HELP_LIST.append(mod)
    help_handler = CommandHandler("help", help, pass_args=True)
    main_dispatcher.add_handler(help_handler)
    unknown_handler = MessageHandler(Filters.command, unknown)
    main_dispatcher.add_handler(unknown_handler)
    unknown_handler = MessageHandler(Filters.text, unknown)
    main_dispatcher.add_handler(unknown_handler)


if __name__ == "__main__":
    logging.info("Demarrage de Bookmaker")
    print(cfg.bot_token)
    updater = Updater(token=cfg.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    charge_plugins(dispatcher)
    # dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

    logging.info("Extinction de Bookmaker")
