import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import time
import os
import requests
import base64

# === CONFIGURATION ===

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'sender': os.getenv('SENDER_EMAIL'),
    'password': os.getenv('SENDER_PASSWORD'),
    'recipient': os.getenv('RECIPIENT_EMAIL')
}

MAX_PER_FEED = int(os.getenv('MAX_PER_FEED', 5))
NAME = os.getenv('RECIPIENT_NAME', 'toi')
SCHEDULE_TIME=os.getenv('SCHEDULE_TIME', '10:00')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_MAX_PER_FEED = int(os.getenv('PODCASTS_MAX_PER_FEED', 3))

RSS_FEEDS_STR = os.getenv('RSS_FEEDS', '')
RSS_FEEDS = [feed.strip() for feed in RSS_FEEDS_STR.split(',') if feed.strip()]

# Flux par défaut si la variable d'environnement est vide
if not RSS_FEEDS:
    RSS_FEEDS = [
        'https://www.lemonde.fr/international/rss_full.xml',
    ]

PODCASTS_FEEDS_STR = os.getenv('PODCASTS_FEEDS', '')
PODCASTS_FEEDS = [feed.strip() for feed in PODCASTS_FEEDS_STR.split(',') if feed.strip()]
show_podcast = False

# === ARTICLES FETCHING ===

def parse_date(entry):
    """Parse la date d'un article avec plusieurs fallbacks"""
    # Essayer published_parsed
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6])
        except:
            pass
    
    # Essayer updated_parsed
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6])
        except:
            pass
    
    # Par défaut, utiliser maintenant
    return datetime.now()

def fetch_recent_articles(MAX_PER_FEED=5):
    """Récupère les articles des dernières X heures (max 5 par flux)"""
    articles = []
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            feed_articles = []
            
            for entry in feed.entries:
                pub_date = parse_date(entry)
                
                if pub_date > cutoff_time:
                    # Garder le titre tel quel (sera échappé dans create_html_email)
                    title = entry.title
                    
                    # Récupérer le résumé de manière sécurisée
                    summary = entry.get('summary', entry.get('description', ''))
                    if summary:
                        # Nettoyer COMPLÈTEMENT les balises HTML du résumé
                        import re
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
            
            # Trier les articles de ce flux par date et prendre les plus récents
            feed_articles.sort(key=lambda x: x['date'], reverse=True)
            articles.extend(feed_articles[:MAX_PER_FEED])
            
        except Exception as e:
            print(f"Erreur avec {feed_url}: {e}")
    

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
        url = f"https://api.spotify.com/v1/shows/{show_id}/episodes"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        params = {
            "limit": SPOTIFY_MAX_PER_FEED
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        episodes = response.json()["items"]

        # Filtrer les épisodes de la veille
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        return [
            episode for episode in episodes
            if datetime.strptime(episode["release_date"], "%Y-%m-%d").date() == yesterday.date()
        ]
    except Exception as e:
            return []
    
def fetch_recent_podcasts():
    """Récupère les podcasts des dernières 24 heures (max X par flux)"""
    podcasts = []
    
    for show_id in PODCASTS_FEEDS:
        try:
            episodes = get_recent_podcast_by_show(show_id)
            
            podcasts.extend(episodes)  
        except Exception as e:
            print(f"Erreur avec le podcast {show_id}: {e}")
    
    return podcasts


# === EMAIL GENERATION AND SENDING ===

def create_html_email(articles, podcasts):
    """Génère le HTML de la newsletter"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            .article {{ margin: 20px 0; padding: 15px; border-left: 3px solid #b52bff; }}
            .source {{ color: #666; font-size: 0.9em; }}
            .summary {{ color: #444; margin-top: 5px; }}
            a {{ color: #7b00ff; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h1>👋 Bonjour {NAME}, voici votre newsletter du {datetime.now().strftime('%d/%m')}</h1>
        <p>{len(articles)} articles des dernières 24h</p>
    """
    
    for article in articles:
        html += f"""
        <div class="article">
            <h3><a href="{article['link']}">{article['title']}</a></h3>
            <p class="source">{article['source']} - {article['date'].strftime('%H:%M')}</p>
            <p class="summary">{article['summary']}...</p>
        </div>
        """

    if show_podcast:
        html += f"""
        <h2>🎧 Podcasts récents</h2>
        <p>{len(podcasts)} épisodes des dernières 24h</p>
        """
        for episode in podcasts:
            html += f"""
            <div class="article">
                <h3><a href="{episode['external_urls']['spotify']}">{episode['name']}</a></h3>
                <p class="source">Podcast - {episode['release_date']}</p>
                <p class="summary">{episode['description'][:50]}...</p>
            </div>"""

    
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
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        print(f"Newsletter envoyée à {datetime.now()}")
    except Exception as e:
        print(f"Erreur d'envoi: {e}")

def generate_newsletter():
    """Génère et envoie la newsletter"""
    print("Génération de la newsletter...")
    articles = fetch_recent_articles(MAX_PER_FEED)
    podcast = fetch_recent_podcasts()
    if len(podcast) > 0:
        show_podcast = True
    if articles:
        html = create_html_email(articles, podcast)
        send_email(html)
    else:
        print("Aucun nouvel article")

# Planification : tous les jours à 6h
schedule.every().day.at(SCHEDULE_TIME).do(generate_newsletter)

if __name__ == "__main__":
    generate_newsletter() # Test immédiat

    # Boucle de planification
    while True:
        schedule.run_pending()
        time.sleep(60)