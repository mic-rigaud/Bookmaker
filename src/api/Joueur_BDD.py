import logging

from peewee import CharField, IntegerField

from src.api.api_bdd import BaseModel


class Joueur(BaseModel):
    """Objet definissant les Joueurs dans la BDD."""

    nom = CharField()
    chat_id = CharField()
    user_id = CharField()
    total_point = IntegerField(default=0)


def get_joueur(chatid, userid):
    """get_joueur: permet de récuperer un joueur"""
    try:
        return (
            Joueur.select()
            .where(Joueur.chat_id == chatid and Joueur.user_id == userid)
            .get()
        )
    except Joueur.DoesNotExist:
        logging.warning(
            "Le joueur demandé n'existe pas. Le chatid est {} et le userid est {}".format(
                chatid, userid
            )
        )
        return None
