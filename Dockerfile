FROM debian

ARG BOOKMAKER_BOT_TOKEN
ARG BOOKMAKER_MDP
ARG BOOKMAKER_ADMIN
ARG RUGBY_API_KEY


RUN apt-get update -yq  \
    && apt-get install -y python3-pip python3 net-tools graphviz traceroute  \
    && apt-get clean -y  \
    && pip3 install poetry

ADD . /app/

WORKDIR /app

VOLUME /app/log
VOLUME /app/ressources

RUN cp ./install/config-docker.py ./config.py && poetry install && poetry run invoke install


CMD poetry run invoke config-bdd && poetry run invoke start-local