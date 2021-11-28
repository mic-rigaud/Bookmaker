# @Author: michael
# @Date:   12-Jan-2018
# @Project: Blueberry
# @Filename: fabfile.py
# @Last modified by:   michael
# @Last modified time: 09-Feb-2021
# @License: GNU GPL v3

from invoke import task

import config as cfg
import src.api.api_bdd as bdd
from src.api.Joueur_BDD import Joueur


@task
def test(c):
    """Lance test unitaire."""
    c.run("python -m pytest", warn=True)


@task
def test_code(c):
    """Lance code security analyse."""
    c.run("black ./")
    c.run("bandit -r ./ -x *config.py,*test*.py", warn=True)


@task
def start_local(c):
    """Lance test unitaire."""
    c.run("python3 main.py", pty=True, warn=True)


@task
def install(c):
    """Install blueberry."""
    config_service(c)
    config_bdd()
    c.run("mkdir log")
    c.run("touch log/bookmaker.log")


@task
def config_service(c):
    """Configure le service Blueberry."""
    c.run(
        'sed -e "s/{{{{dir}}}}/{}/g" install/bookmaker.service >> /etc/systemd/system/bookmaker.service'.format(
            cfg.work_dir.replace("/", "\/")
        )
    )
    c.run("chown root: /etc/systemd/system/bookmaker.service", warn=True)


@task
def config_bdd(c):
    """Permet l'installation de la BDD automatise."""
    try:
        var = bdd.db.connect
        bdd.db.create_tables([Joueur])
    except:
        print("=== La base SQL existe déjà ===")
