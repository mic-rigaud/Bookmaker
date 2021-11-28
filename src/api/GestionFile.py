import json
import logging


def file_get_next(file, id):
    """Lister les éléments d'un fichier."""
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        return str(id), contenu[str(id)]
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        raise FileNotFoundError


def file_get_max(file):
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        return len(contenu)
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        raise FileNotFoundError


def file_get(file, id):
    """Recuperer un element a partir de l id."""
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        if contenu == "":
            logging.warning("Aucun element dans le fichier {0}".format(file))
            raise Exception("fichier vide")
        return contenu[id]
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        raise FileNotFoundError("Le fichier n'existe pas")
    except ValueError as e:
        logging.error("Entre n est pas un int: {}".format(e))
        raise ValueError("<b>Veuiller entrer un int</b>")


def file_get_all(file):
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        if contenu == "":
            logging.warning("Aucun element dans le fichier {0}".format(file))
            raise Exception("fichier vide")
        return contenu
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        raise FileNotFoundError("Le fichier n'existe pas")
    except ValueError as e:
        logging.error("Entre n est pas un int: {}".format(e))
        raise ValueError("<b>Veuiller entrer un int</b>")
