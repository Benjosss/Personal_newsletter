# 📰 Personal RSS Newsletter

> Agrégateur RSS personnalisé avec support Spotify Podcasts - Newsletter quotidienne automatique

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()


Recevez chaque matin une newsletter personnalisée construite à partir de vos sources d’information.  
Vous choisissez vos flux RSS et vos podcasts → le système les agrège → vous recevez une newsletter propre, concise et sans publicité.

## ✨ Fonctionnalités  

[![RSS](https://img.shields.io/badge/RSS-Integration-orange.svg)]()  
[![Spotify](https://img.shields.io/badge/Spotify-Integrated-green.svg)]()  

- 🎯 Agrégation multi-sources RSS
- 🎧 Intégration podcasts Spotify
- 📧 Email HTML responsive
- ⚙️ Interface de configuration visuelle
- 🐳 Déploiement Docker simplifié
- 🔒 Variables d'environnement sécurisées



## 🧱 Architecture
| Composant | Rôle |
| :---------------: |:---------------:|
| newsletter.py  | Récupère les flux et génère la newsletter en HTML |  
| docker-compose.yml | Conteneurisation et planification d’exécution | 
| newsletter_config.exe | Lancemenent d'une interface web pour la configuration des emails |
| config.py | La même chose mais directement en .py |  
| .env | Configuration privée (emails, flux, planification) |  

## 🔧 Prérequis

- Python 3.9+

- pip

- (Optionnel) Docker et Docker Compose

- Un compte email SMTP (Gmail recommandé, App Password conseillé)

- (Optionnel) Clés d'application Spotify

## 🚀 Installation rapide

### Option 1 : Avec Docker (recommandé)
```bash
git clone https://github.com/Benjosss/Personal_newsletter
cd Personal_newsletter
python config.py  # Configure via interface web
# ou exécution de config.exe
docker-compose build
docker-compose up -d
```

### Option 2 : Installation locale
```bash
git clone https://github.com/Benjosss/Personal_newsletter
cd Personal_newsletter
pip install -r requirements.txt
python config.py  # Configure via interface web
# ou exécution de config.exe
python newsletter.py
```

## ⚙️ Paramètres configurables

### Email
> Serveur SMTP (smtp.gmail.com par défaut )  
> Port SMTP (587 par défaut)  
  
> Email expéditeur  
> Mot de passe d'application (vidéo tutorielle dans l'interface web)  
> Email destinataire  
> Prénom destinataire  
  
### Planification  
> Heure d'envoi (HH:MM)  


### Flux RSS  
> Nombre d'articles par sources RSS  
> URLs des flux RSS (séparés par des virugles)  

### Podcasts Spotify  
> Spotify Client ID  
> Spotify Client Secret (Tuto dans l'interface web)  
> Id des podcasts Spotify (Tuto dans l'interface web)  


## 🏗️ Architecture
```
newsletter-rss/
├── config.py              # Interface de configuration
├── newsletter_config.exe  # Interface de configuration (.exe)
├── newsletter.py          # Script principal d'envoi d'email
├── web_config/            # Frontend React
├── Dockerfile             # Image Docker
├── docker-compose.yml     # Orchestration
└── build.py               # Permet de packager les modification sur config.py
```

## 🛠️ Stack technique

- **Backend** : Python 3.9+, feedparser, schedule, requests, dotenv
- **Frontend** : React, TailwindCSS
- **APIs** : Spotify Web API, SMTP
- **DevOps** : Docker, docker-compose

## 🤝 Contribution

Les PRs sont les bienvenues !

## 📄 License

MIT © [LALLEMENT Benjamin]