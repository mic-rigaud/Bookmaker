from peewee import CharField, IntegerField

from src.api.api_bdd import BaseModel


class Joueur(BaseModel):
    """Objet definissant une IP pour la BDD."""

    nom = CharField()
    chat_id = CharField()
    total_point = IntegerField(default=0)
