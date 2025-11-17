from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from html import escape
import smtplib
import base64
import sys
import time
import os
import re

import requests
import schedule
import feedparser
from dotenv import load_dotenv
load_dotenv()

# === CONFIGURATION TESTS ===

class ConfigValidator:
    def __init__(self):
        self.valid = True
        self.errors = []
    
    def add_error(self, message):
        self.valid = False
        self.errors.append(message)
    
    def test_email(self, mail, field_name):
        if not mail:
            self.add_error(f"{field_name} est obligatoire")
            return
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail)
        if not valid:
            self.add_error(f"{field_name} invalide : {mail}")
    
    def test_smtp_server(self, smtp):
        if not smtp:
            return  # Optional
        valid = re.match(r'^([a-zA-Z0-9_%+-]+\.)+[a-zA-Z]{2,}$', smtp)
        if not valid:
            self.add_error(f"Serveur SMTP invalide : {smtp}")
    
    def test_smtp_port(self, port):
        if not port:
            return  # Optional
        try:
            port_int = int(port)
            if port_int <= 0:
                self.add_error(f"Port SMTP doit être positif : {port}")
        except (ValueError, TypeError):
            self.add_error(f"Port SMTP invalide : {port}")
    
    def test_app_password(self, password):
        if not password:
            self.add_error("Mot de passe d'application est obligatoire")
            return
        password_clean = password.replace(' ', '')
        valid = re.match(r'^[a-z]{16}$', password_clean)
        if not valid:
            self.add_error(f"Mot de passe d'application Gmail invalide (format attendu : xxxx xxxx xxxx xxxx)")
    
    def test_name(self, name):
        if not name:
            return  # Optional
        valid = re.match(r'^[a-zA-Z0-9\u00C0-\u00FF\'\-\s]+$', name)
        if not valid:
            self.add_error(f"Nom invalide : {name}")
    
    def test_max_feed(self, max_feed):
        if not max_feed:
            return  # Optional
        try:
            max_int = int(max_feed)
            if max_int <= 0:
                self.add_error(f"Nombre de flux max doit être positif : {max_feed}")
        except (ValueError, TypeError):
            self.add_error(f"Nombre de flux max invalide : {max_feed}")
    
    def test_time(self, time_str):
        if not time_str:
            return  # Optional
        valid = re.match(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$', time_str)
        if not valid:
            self.add_error(f"Heure d'envoi invalide (format HH:MM attendu) : {time_str}")
    
    def test_spotify_client(self, client, field_name):
        if not client:
            return  # Optional
        valid = re.match(r'^[a-zA-Z0-9]{32}$', client)
        if not valid:
            self.add_error(f"{field_name} invalide (32 caractères alphanumériques attendus) : {client}")
    
    def test_rss_feeds(self, feeds_str):
        if not feeds_str:
            return  # Optional
        
        feeds = [f.strip() for f in feeds_str.split(',') if f.strip()]
        for feed in feeds:
            valid = re.match(r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/=]*)$', feed)
            if not valid:
                self.add_error(f"Flux RSS invalide : {feed}")
    
    def test_podcast_feeds(self, feeds_str):
        if not feeds_str:
            return  # Optional
        
        feeds = [f.strip() for f in feeds_str.split(',') if f.strip()]
        for feed in feeds:
            valid = re.match(r'^[a-zA-Z0-9]{22}$', feed)
            if not valid:
                self.add_error(f"ID Podcast Spotify invalide (22 caractères attendus) : {feed}")

# === LOADING AND CONFIGURATION VALIDATION ===

validator = ConfigValidator()

# Required
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '').strip()
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '').strip()
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', '').strip()

validator.test_email(SENDER_EMAIL, "Email expéditeur")
validator.test_app_password(SENDER_PASSWORD)
validator.test_email(RECIPIENT_EMAIL, "Email destinataire")

# Optionals and defaults
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com').strip() or 'smtp.gmail.com'
SMTP_PORT = os.getenv('SMTP_PORT', '587').strip() or '587'
MAX_PER_FEED = os.getenv('MAX_PER_FEED', '5').strip() or '5'
NAME = os.getenv('RECIPIENT_NAME', 'toi').strip() or 'toi'
SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', '10:00').strip() or '10:00'
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '').strip()
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '').strip()
RSS_FEEDS_STR = os.getenv('RSS_FEEDS', '').strip()
PODCASTS_FEEDS_STR = os.getenv('PODCASTS_FEEDS', '').strip()

# Optionals validation
validator.test_smtp_server(SMTP_SERVER)
validator.test_smtp_port(SMTP_PORT)
validator.test_max_feed(MAX_PER_FEED)
validator.test_name(NAME)
validator.test_time(SCHEDULE_TIME)
validator.test_spotify_client(SPOTIFY_CLIENT_ID, "Spotify Client ID")
validator.test_spotify_client(SPOTIFY_CLIENT_SECRET, "Spotify Client Secret")
validator.test_rss_feeds(RSS_FEEDS_STR)
validator.test_podcast_feeds(PODCASTS_FEEDS_STR)

# Errors
if not validator.valid:
    print("❌ ERREUR DE CONFIGURATION")
    print("=" * 50)
    for error in validator.errors:
        print(f"  • {error}")
    print("=" * 50)
    print("\n💡 Vérifiez votre fichier .env et relancez le script")
    print("   Ou exécutez : python config.py\n")
    sys.exit(1)

# Type casts
MAX_PER_FEED = int(MAX_PER_FEED)
SMTP_PORT = int(SMTP_PORT)

# Email config
EMAIL_CONFIG = {
    'smtp_server': SMTP_SERVER,
    'smtp_port': SMTP_PORT,
    'sender': SENDER_EMAIL,
    'password': SENDER_PASSWORD,
    'recipient': RECIPIENT_EMAIL
}

# RSS feed default
RSS_FEEDS = [feed.strip() for feed in RSS_FEEDS_STR.split(',') if feed.strip()]
if not RSS_FEEDS:
    RSS_FEEDS = ['https://www.lemonde.fr/international/rss_full.xml']

# Podcasts (optional)
PODCASTS_FEEDS = [feed.strip() for feed in PODCASTS_FEEDS_STR.split(',') if feed.strip()]

# Podcast check
PODCASTS_ENABLED = bool(SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and PODCASTS_FEEDS)

print("✅ CONFIGURATION VALIDE")
print("=" * 50)
print(f"📧 Expéditeur : {SENDER_EMAIL}")
print(f"📬 Destinataire : {RECIPIENT_EMAIL}")
print(f"👤 Nom : {NAME}")
print(f"⏰ Heure d'envoi : {SCHEDULE_TIME}")
print(f"📰 Flux RSS : {len(RSS_FEEDS)} source(s)")
print(f"🎧 Podcasts : {'Activé' if PODCASTS_ENABLED else 'Désactivé'} ({len(PODCASTS_FEEDS)} show(s))")
print(f"📊 Max articles/flux : {MAX_PER_FEED}")
print("=" * 50 + "\n")

# === ARTICLES FETCHING ===

def parse_date(entry):
    """Parse la date d'un article avec plusieurs fallbacks"""
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6])
        except:
            pass
    
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6])
        except:
            pass
    
    return datetime.now()

def fetch_recent_articles(max_per_feed=5):
    """Récupère les articles des dernières 24 heures"""
    articles = []
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            feed_articles = []
            
            for entry in feed.entries:
                pub_date = parse_date(entry)
                
                if pub_date > cutoff_time:
                    title = entry.title
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    if summary:
                        from html.parser import HTMLParser
                        
                        class HTMLStripper(HTMLParser):
                            def __init__(self):
                                super().__init__()
                                self.reset()
                                self.strict = False
                                self.convert_charrefs = True
                                self.text = []
                            def handle_data(self, d):
                                self.text.append(d)
                            def get_data(self):
                                return ''.join(self.text)
                        
                        stripper = HTMLStripper()
                        stripper.feed(summary)
                        summary = stripper.get_data()
                        summary = summary.strip()[:50]
                    
                    feed_articles.append({
                        'title': title,
                        'link': entry.link,
                        'source': feed.feed.get('title', 'Source inconnue'),
                        'date': pub_date,
                        'summary': summary
                    })
            
            feed_articles.sort(key=lambda x: x['date'], reverse=True)
            articles.extend(feed_articles[:max_per_feed])
            
        except Exception as e:
            print(f"⚠️  Erreur avec {feed_url}: {e}")
    
    return articles

# === PODCASTS FETCHING ===

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_recent_podcast_by_show(show_id):
    try:
        access_token = get_access_token()
        
        show_url = f"https://api.spotify.com/v1/shows/{show_id}"
        show_response = requests.get(show_url, headers={"Authorization": f"Bearer {access_token}"})
        show_response.raise_for_status()
        show_name = show_response.json()["name"]
        
        url = f"https://api.spotify.com/v1/shows/{show_id}/episodes"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": 50}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        episodes = response.json()["items"]

        today = datetime.now().date()
        yesterday = (datetime.now() - timedelta(days=1)).date()
        
        filtered_episodes = []
        for episode in episodes:
            release_date = datetime.strptime(episode["release_date"], "%Y-%m-%d").date()
            if release_date == today or release_date == yesterday:
                episode['show_name'] = show_name
                filtered_episodes.append(episode)
        
        return filtered_episodes
        
    except Exception as e:
        print(f"⚠️  Erreur podcast {show_id}: {e}")
        return []

def fetch_recent_podcasts():
    if not PODCASTS_ENABLED:
        return []
    
    podcasts = []
    for show_id in PODCASTS_FEEDS:
        try:
            episodes = get_recent_podcast_by_show(show_id)
            podcasts.extend(episodes)
        except Exception as e:
            print(f"⚠️  Erreur avec podcast {show_id}: {e}")
    
    return podcasts

# === EMAIL GENERATION ===

def create_html_email(articles, podcasts):    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{ 
            color: #333; 
            text-align: center;
        }}
        .articles-title {{
            color: #333;
            margin-top: 40px;
            border-bottom: 2px solid #b52bff;
            padding-bottom: 10px;
        }}
        .podcasts-title {{
            color: #333;
            margin-top: 40px;
            border-bottom: 2px solid #345beb;
            padding-bottom: 10px;
        }}
        .article {{ 
            margin: 20px 0; 
            padding: 15px; 
            border-left: 4px solid #b52bff;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .article h3 {{
            margin-top: 0;
            margin-bottom: 10px;
        }}
        .podcast {{ 
            margin: 20px 0; 
            padding: 15px; 
            border-left: 4px solid #345beb;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .podcast h3 {{
            margin-top: 0;
            margin-bottom: 10px;
        }}
        .source {{ 
            color: #666; 
            font-size: 0.9em; 
            margin-bottom: 8px;
        }}
        .summary {{ 
            color: #444; 
            margin-top: 8px;
            line-height: 1.5;
        }}
        a {{ 
            text-decoration: none; 
        }}
        .article a {{ color: #b52bff; }}
        .podcast a {{ color: #345beb; }}
        a:hover {{ text-decoration: underline; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>👋 Bonjour {escape(NAME)}, voici votre newsletter du {datetime.now().strftime('%d/%m')}</h1>
        <p>{len(articles)} article(s) des dernières 24h</p>
    </div>

    <h2 class="articles-title">📰 Articles récents</h2>
"""
    
    for article in articles:
        title_safe = escape(article['title'])
        source_safe = escape(article['source'])
        summary_safe = escape(article['summary']) if article['summary'] else ''
        link_safe = escape(article['link'])
        
        html += f"""
    <div class="article">
        <h3><a href="{link_safe}">{title_safe}</a></h3>
        <p class="source">{source_safe} • {article['date'].strftime('%H:%M')}</p>
        <p class="summary">{summary_safe}...</p>
    </div>
"""

    if len(podcasts) > 0:
        html += f"""
    <h2 class="podcasts-title">🎧 Podcasts récents</h2>
    <p>{len(podcasts)} épisode(s) des dernières 24h</p>
"""
        for episode in podcasts:
            try:
                episode_title = escape(episode.get('name', 'Sans titre'))
                episode_url = escape(episode.get('external_urls', {}).get('spotify', '#'))
                
                # Gestion sécurisée de la description
                description = episode.get('description', '')
                if description:
                    episode_desc = escape(description[:200])
                else:
                    episode_desc = ''
                
                episode_date = episode.get('release_date', 'Date inconnue')
                episode_duration_min = episode.get('duration_ms', 0) // 60000
                episode_show = escape(episode.get('show_name', 'Podcast'))
                
                html += f"""
    <div class="podcast">
        <h3><a href="{episode_url}">{episode_title}</a></h3>
        <p class="source">{episode_show} • {episode_date} • {episode_duration_min}min</p>
        {'<p class="summary">' + episode_desc + '...</p>' if episode_desc else ''}
    </div>
"""
            except Exception as e:
                print(f"⚠️  Erreur lors du formatage d'un podcast: {e}")
                continue
    
    html += """
</body>
</html>
"""
    return html

def send_email(html_content):
    """Envoie l'email"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Newsletter - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To'] = EMAIL_CONFIG['recipient']
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        print(f"✅ Newsletter envoyée à {datetime.now()}")
    except Exception as e:
        print(f"❌ Erreur d'envoi: {e}")

def generate_newsletter():
    """Génère et envoie la newsletter"""
    print(f"\n📬 Génération de la newsletter - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    articles = fetch_recent_articles(MAX_PER_FEED)
    podcasts = fetch_recent_podcasts()
    
    print(f"📰 {len(articles)} article(s) trouvé(s)")
    print(f"🎧 {len(podcasts)} podcast(s) trouvé(s)")

    if articles or podcasts:
        html = create_html_email(articles, podcasts)
        send_email(html)
    else:
        print("ℹ️  Aucun contenu à envoyer")

# === MAIN ===

if __name__ == "__main__":
    # Test
    generate_newsletter()
    
    # Schedule
    schedule.every().day.at(SCHEDULE_TIME).do(generate_newsletter)
    
    print(f"⏰ Newsletter planifiée tous les jours à {SCHEDULE_TIME}")
    print("🔄 En attente... (Ctrl+C pour arrêter)\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 Arrêt du script")