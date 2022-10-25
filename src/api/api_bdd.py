from peewee import Model
from playhouse.sqlite_ext import SqliteDatabase

import config as cfg


db = SqliteDatabase(f"{cfg.work_dir}ressources/bdd.db")


class BaseModel(Model):
    """Classe BaseModel."""

    class Meta:
        """Classe Meta."""

        database = db
