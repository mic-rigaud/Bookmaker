from peewee import BooleanField, DateTimeField, ForeignKeyField, IntegerField

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
    date_match = DateTimeField(formats="%Y-%m-%d %H:%M:%S")

    def afficher_paris(self):
        """afficher_paris:"""
        reponse = f"<b>{self.match.equipe1} - {self.match.equipe2}</b>\n"
        match_board = {1: self.match.equipe1, 2: self.match.equipe2}
        # noinspection PyTypeChecker
        reponse += f"  Vainqueur: {match_board[int(self.vainqueur)]}"
        if self.bonus_offensif:
            reponse += "\n  Avec bonus Offensif"
        if self.bonus_defensif:
            reponse += "\n  Avec bonus Defensif"

        if self.match.vainqueur != 0:
            reponse += f"\n<b>Match terminé. Vaiqueur: {match_board[int(self.match.vaiqueur)]}{' Bo' if self.match.bonus_offensif else ''}{' Bd' if self.match.bonus_defensif else ''}<b>"
        return reponse
