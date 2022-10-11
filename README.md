![Gitlab](https://gitlab.com/mic-rigaud/Bookmaker/badges/main/pipeline.svg)

# Bookmaker

Bot telegram pour des paris rugbystiques entre amis à héberger chez soi

ATTENTION : Ce Bot n'est pas terminé. Et il n'est pas encore opérationnel.

## Docker

Préparer l'installation:

```bash
cp ./test/install/config.test ./config.py
```

Ensuite il faut modifier le fichier config.py

```bash
docker build -t bookmaker
docker volume create bookmaker-log
docker volume create bookmaker-data
``` 

Puis pour lancer le container:

```bash
docker run -d -v bookmaker-log:/app/log -v bookmaker-data:/app/ressources bookmaker
```

## Standalone

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