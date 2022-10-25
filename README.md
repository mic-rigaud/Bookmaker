![Gitlab](https://gitlab.com/mic-rigaud/Bookmaker/badges/main/pipeline.svg)

# Bookmaker

Version: 0.1.0

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
cp ./test/install/config.test ./config.py
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
cp ./test/install/config.test ./config.py
poetry run invoke install
```

Il faut modifier le fichier config.py.

Enfin, pour lancer l'application

```bash
poetry run invoke start-local
```