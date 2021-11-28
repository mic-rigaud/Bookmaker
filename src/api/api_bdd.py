from peewee import Model
from playhouse.sqlite_ext import SqliteDatabase

import config as cfg

db = SqliteDatabase(cfg.work_dir + "bdd.db")


class BaseModel(Model):
    """Classe BaseModel."""

    class Meta:
        """Classe Meta."""

        database = db
