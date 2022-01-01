from datetime import datetime

from peewee import CharField, IntegerField, BooleanField, DateTimeField
from telegram import InlineKeyboardButton

from src.api.api_bdd import BaseModel


class Match(BaseModel):
    """Objet definissant un match dans la BDD."""

    match_id = CharField()
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

    def __str__(self):
        return "{} - {}".format(self.equipe1, self.equipe2)


def liste_next_match():
    """liste_match: renvoi un dictionnaire des prochain match"""
    return {
        match.get_id(): str(match)
        for match in Match.select().where(Match.date_match > datetime.now())
    }


def creer_button_liste_next_match(patern):
    """creer_button_liste_next_match:"""
    return [
        InlineKeyboardButton(valeur, callback_data="{}_{}".format(patern, key))
        for key, valeur in liste_next_match().items()
    ]
