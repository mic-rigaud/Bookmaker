from peewee import IntegerField, DateTimeField, CharField

from src.api.api_bdd import BaseModel


class Saisons(BaseModel):
    """Objet definissant les saisons de rugby suivis par le bot."""

    nom = CharField()
    season_id = IntegerField()
    expiration = DateTimeField()
