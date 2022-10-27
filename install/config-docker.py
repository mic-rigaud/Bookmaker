# Il faut completer ce fichier puis le renommer config.py

import os


# Tokens du Bot Telegram
bot_token = os.environ['BOOKMAKER_BOT_TOKEN']

# Administrateurs
# Liste des personnes autorisées a administrer le bot.
# il est attendu les chat_id des administrateurs
admin_chatid = [os.environ['BOOKMAKER_ADMIN']]

# Mot de passe pour pouvoir acceder à ce bot
mdp = os.environ['BOOKMAKER_MDP']

# Log
# Position du fichier de Log
log = "/app/log/bookmaker.log"
work_dir = "/app/"
# Pour une utilisation avec Docker, utiliser ces variables:
# log = "/app/log/bookmaker.log"
# work_dir = "/app/"


# API_KEY
# L'api de sportradar est utilisé. Une clef gratuite est suffisante pour avoir une
# actualisation par jour. Attention, il faut une clef pour l'api rugby union
rugby_api_key = os.environ['RUGBY_API_KEY']

# Configuration du nombre de point gagné par les joueurs
pts_paris_gagnant = 3
pts_bonus_offensif = 1
pts_bonus_defensif = 1

## Variable a passer a True en phase de test pour diminuer le nombre d'appel API
test = False
