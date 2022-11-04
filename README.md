![version](https://img.shields.io/badge/version-0.1.0-success) [![Python application](https://github.com/mic-rigaud/Bookmaker/actions/workflows/python-app.yml/badge.svg)](https://github.com/mic-rigaud/Bookmaker/actions/workflows/python-app.yml) [![CodeQL](https://github.com/mic-rigaud/Bookmaker/actions/workflows/codeql.yml/badge.svg)](https://github.com/mic-rigaud/Bookmaker/actions/workflows/codeql.yml/badge.svg)

# Bookmaker

This bot speak in french. It is a bot for french people. So the rest of this README is in french.

## Description

Bot telegram pour des paris rugbystiques entre amis à héberger chez soi

*ATTENTION : Ce Bot fonctionne mais c'est une version Beta*

## Prérequis

Attention, pour utiliser ce bot il faut au préalable :

- Avoir un créé un bot télégram avec le [Bot Father](https://botostore.com/c/botfather/)
- Avoir une clef pour utiliser l'[API](https://api.sportradar.us/rugby-union/) Rugby Union de Sportradar. Avec l'API
  gratuite le nombre de requete est limité. C'est suffisant pour un usage personnel uniquement.

## Installation

### Docker

Préparer l'installation:

```bash
cp ./install/config.test ./config.py
```

OU

mais dans ce cas il faut préciser les variables d'environnements lors du lancement du docker

```bash
cp ./install/config-docker.py ./config.py
```

Ensuite il faut modifier le fichier config.py

```bash
docker volume create bookmaker-log
docker volume create bookmaker-data
docker build -t bookmaker .
``` 

Puis pour lancer le container:

```bash
docker run -d -v bookmaker-log:/app/log -v bookmaker-data:/app/ressources bookmaker
```

### Standalone

Pour preparer l'installation

```bash
apt-get update -qq && apt-get install -y python3-pip python3 net-tools graphviz traceroute
pip3 install poetry
poetry install
cp ./install/config.test ./config.py
poetry run invoke install
```

Il faut modifier le fichier config.py.

Enfin, pour lancer l'application

```bash
poetry run invoke start-local
```

## Report un problème de sécurité

Veuillez consulter le [Security.md](./Security.md)