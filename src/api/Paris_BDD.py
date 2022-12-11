from datetime import datetime
import logging

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
    points_gagnes = IntegerField(default=0)

    def afficher_paris(self):
        """afficher_paris:"""
        reponse = f"<b>{self.match.equipe1} - {self.match.equipe2}</b>\n"
        match_board = {1: self.match.equipe1, 2: self.match.equipe2}
        reponse += f"  <i>{self.get_date_paris():%d/%m/%Y %H:%M}</i>\n"
        # noinspection PyTypeChecker
        reponse += f"  Vainqueur: {match_board[int(self.vainqueur)]}"
        if self.bonus_offensif:
            reponse += "\n  Avec bonus Offensif"
        if self.bonus_defensif:
            reponse += "\n  Avec bonus Defensif"

        if self.match.vainqueur != 0:
            if self.match.vainqueur == 3:
                reponse += f"\n<b>TERMINE. EGALITE"
            else:
                reponse += f"\n<b>TERMINE. V: {match_board[int(self.match.vainqueur)]}"
            reponse += f"{' -Bo' if self.match.bonus_offensif else ''}"
            reponse += f"{' -Bd' if self.match.bonus_defensif else ''}"
            reponse += f" (+{self.points_gagnes} pts)</b>\n"
        return reponse

    def get_date_paris(self):
        # noinspection PyTypeChecker
        return datetime.strptime(self.date_match, "%Y-%m-%d %H:%M:%S%z")


def get_paris(joueur, match):
    """get_paris: retourne le paris avec un joueur et un match_id

    :param Joueur joueur: joueur de la recherche
    :param Match match: match de la recherche
    :rtype: Paris
    """

    try:
        return (
            Paris.select().where((Paris.joueur == joueur) & (Paris.match == match)).get()
        )
    except Paris.DoesNotExist:
        logging.warning(
                f"Le joueur demandé n'existe pas. Le joueur est {joueur.nom} et le match_id est {match.match_id}")
        return None
