FROM debian

RUN apt-get update -yq  \
    && apt-get install -y python3-pip python3 net-tools graphviz traceroute  \
    && apt-get clean -y  \
    && pip3 install poetry

ADD . /app/

WORKDIR /app

VOLUME /app/log
VOLUME /app/ressources

RUN poetry install && poetry run invoke install


CMD poetry run invoke config-bdd && poetry run invoke start-local