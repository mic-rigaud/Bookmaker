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

    def afficher_paris(self):
        """afficher_paris:"""
        reponse = "<b>{} - {}</b>\n".format(self.match.equipe1, self.match.equipe2)
        match_board = {1: self.match.equipe1, 2: self.match.equipe2}
        reponse += "  Vainqueur: {}\n".format(match_board[int(self.vainqueur)])
        if self.bonus_offensif:
            reponse += "  Avec bonus Offensif"
        if self.bonus_defensif:
            reponse += "  Avec bonus Defensif"
        return reponse
