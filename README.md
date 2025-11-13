# 📬 Personal Newsletter - Agrégateur RSS Personnalisé

_⚠️ De nouvelles fonctionnalités et une amélioration du style arrivent bientôt !⚠️_  

Recevez chaque matin une newsletter personnalisée construite à partir de vos sources d’information.  
Vous choisissez vos flux RSS et vos podcasts → le système les agrège → vous recevez une newsletter propre, concise et sans publicité.

# ✨ Fonctionnalités

- Ajout simple de flux RSS (Le Monde, Frandroid, JV.com, etc.)

- Ajout simple de vos podcasts Spotify

- Filtrage automatique des articles récents (24h par défaut)

- Filtrage automatique des podcasts récents

- Résumés courts & lisibles

- Envoi d’un email quotidien à une heure définie

- Compatible multi-sources (pas de limite technique)

- S’exécute dans Docker, sur serveur, ou localement

# 🧱 Architecture
| Composant | Rôle |
| :---------------: |:---------------:|
| newsletter.py  | Récupère les flux et génère la newsletter en HTML |  
| docker-compose.yml | Conteneurisation et planification d’exécution |   
| .env | Configuration privée (emails, flux, planification) |  

## 🔧 Prérequis

- Python 3.9+

- pip ou poetry

- (Optionnel) Docker et Docker Compose

- Un compte email SMTP (Gmail recommandé, App Password conseillé)

- (Optionnel) Clés d'application Spotify

# 🗂️ Installation

## Clone du projet :

```
git clone https://github.com/Benjosss/Personal-newsletter.git
cd Personal-newsletter
``` 


## Installe les dépendances :

```
pip install -r requirements.txt
```

## ⚙️ Configuration

Crée un fichier .env à la racine sur le même modèle que .env.example :

### Nombre max d’articles par flux
```
MAX_PER_FEED=5
```
De même pour le nombre de podcasts

### Heure d’envoi quotidienne (HH:MM)
```
SCHEDULE_TIME=06:00
```

### Liste des flux, séparés par des virgules (pas d'espaces)
```
RSS_FEEDS=https://www.frandroid.com/feed,https://www.developpez.com/index/rss,https://journalducoin.com/feed/
```
Faire de même pour les ids de podcasts

### Clé client et mot de passe Spotify
```
SPOTIFY_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SPOTIFY_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### SMTP
```
SENDER_EMAIL=ton_email@gmail.com
SENDER_PASSWORD=motdepasse_ou_app_password
RECIPIENT_EMAIL=destinataire@gmail.com
RECIPIENT_NAME=toi
```

# ▶️ Exécution
## Mode local (test immédiat)
```
python newsletter.py
```

## Mode cron / tâche planifiée

Le script intègre déjà une boucle interne, rien à ajouter.

## 🐳 Exécution avec Docker

Lancer en mode service (`-d` pour détaché) :

```
docker compose up -d
```


Reconstruction si modifications :

```
docker compose down
docker compose up --build -d
```

# 📦 Structure du projet
```
.
├── newsletter.py          # Script principal
├── requirements.txt       # Dépendances Python
├── docker-compose.yml     # Déploiement Docker
├── Dockerfile             # Image Python
└── .env                   # Configuration privée (non commit)
```

# 🧑‍💻 Contribution

Les PR sont les bienvenues : améliorations du parsing RSS, UI, ajout de sources, etc.

# 📄 Licence

MIT — libre d’utilisation, de modification et de distribution.
