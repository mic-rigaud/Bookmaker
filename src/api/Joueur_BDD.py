from peewee import CharField, IntegerField

from src.api.api_bdd import BaseModel


class Joueur(BaseModel):
    """Objet definissant les Joueurs dans la BDD."""

    nom = CharField()
    chat_id = CharField()
    user_id = CharField()
    total_point = IntegerField(default=0)
