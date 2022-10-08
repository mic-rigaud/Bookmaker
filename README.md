![Gitlab](https://gitlab.com/mic-rigaud/Bookmaker/badges/main/pipeline.svg)

# Bookmaker

Bot telegram pour des paris rugbystiques entre amis à héberger chez soi

ATTENTION : Ce Bot n'est pas terminé. Et il n'est pas encore opérationnel.

## Docker

Préparer l'installation:

```bash
docker build -t bookmaker
docker volume create bookmaker-log
docker volume create bookmaker-data
``` 

Puis pour lancer le container:

```bash
docker run -d -v bookmaker-log:/app/log -v bookmaker-data:/app/ressources bookmaker
```