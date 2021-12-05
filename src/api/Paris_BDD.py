from peewee import ForeignKeyField, IntegerField, BooleanField

from src.api.Joueur_BDD import Joueur
from src.api.Match_BDD import Match
from src.api.api_bdd import BaseModel


class Paris(BaseModel):
    """Objet definissant la liste des paris la BDD."""

    joueur = ForeignKeyField(Joueur, backref="paris")
    match = ForeignKeyField(Match, backref="paris")
    vainqueur = IntegerField()
    bonus_offensif = BooleanField(default=False)
    bonus_defensif = BooleanField(default=False)
