from peewee import CharField, IntegerField, BooleanField, DateTimeField

from src.api.api_bdd import BaseModel


class Match(BaseModel):
    """Objet definissant un match dans la BDD."""

    equipe1 = CharField()
    equipe1_code = CharField(default="")
    equipe2 = CharField()
    equipe2_code = CharField(default="")
    date_match = DateTimeField()
    vainqueur = IntegerField(default=0)
    resultat_equipe1 = IntegerField(default=0)
    resultat_equipe2 = IntegerField(default=0)
    bonus_offensif = BooleanField(default=False)
    bonus_defensif = BooleanField(default=False)
