import http.server
import socketserver
import webbrowser
import os
import sys
import json
import threading
import time
from datetime import datetime, timedelta

PORT = 8765
should_shutdown = False
last_activity = datetime.now()
activity_timeout = 600  # Arrêter après 10 minutes d'inactivité

def get_base_path():
    """Retourne le chemin de base selon le mode (exécutable ou script)"""
    if getattr(sys, 'frozen', False):
        # Mode exécutable
        return os.path.dirname(sys.executable)
    else:
        # Mode script
        return os.path.dirname(os.path.abspath(__file__))

def get_env_path():
    """Retourne le chemin absolu du fichier .env"""
    base_dir = get_base_path()
    return os.path.join(base_dir, '.env')

def get_web_root():
    """Retourne le chemin vers les fichiers web"""
    base_dir = get_base_path()
    
    # Essayer d'abord dans le répertoire de base (mode développement)
    web_config_dir = os.path.join(base_dir, 'web_config')
    if os.path.exists(web_config_dir):
        return web_config_dir
    
    # Mode exécutable - chercher dans les données embarquées
    if getattr(sys, 'frozen', False):
        # Essayer web_config d'abord
        temp_web_config = os.path.join(sys._MEIPASS, 'web_config')
        if os.path.exists(temp_web_config):
            return temp_web_config
        
        # Essayer temp_config comme fallback
        temp_config_dir = os.path.join(sys._MEIPASS, 'temp_config')
        if os.path.exists(temp_config_dir):
            return temp_config_dir
    
    return web_config_dir  # Retourner le chemin même s'il n'existe pas

def parse_env_file(env_path):
    """Parse le fichier .env existant"""
    config = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def env_to_config(env_dict):
    """Convertit le format .env en format config JS"""
    return {
        'smtpServer': env_dict.get('SMTP_SERVER', 'smtp.gmail.com'),
        'smtpPort': env_dict.get('SMTP_PORT', '587'),
        'senderEmail': env_dict.get('SENDER_EMAIL', ''),
        'senderPassword': env_dict.get('SENDER_PASSWORD', ''),
        'recipientEmail': env_dict.get('RECIPIENT_EMAIL', ''),
        'recipientName': env_dict.get('RECIPIENT_NAME', ''),
        'scheduleTime': env_dict.get('SCHEDULE_TIME', '06:00'),
        'maxPerFeed': env_dict.get('MAX_PER_FEED', '5'),
        'rssFeeds': env_dict.get('RSS_FEEDS', ''),
        'podcastsFeeds': env_dict.get('PODCASTS_FEEDS', ''),
        'spotifyClientId': env_dict.get('SPOTIFY_CLIENT_ID', ''),
        'spotifyClientSecret': env_dict.get('SPOTIFY_CLIENT_SECRET', '')
    }

def config_to_env(config):
    """Convertit le format config JS en format .env"""
    return f"""# Configuration Email
SMTP_SERVER={config.get('smtpServer', 'smtp.gmail.com')}
SMTP_PORT={config.get('smtpPort', '587')}
SENDER_EMAIL={config.get('senderEmail', '')}
SENDER_PASSWORD={config.get('senderPassword', '')}
RECIPIENT_EMAIL={config.get('recipientEmail', '')}

# Personnalisation
RECIPIENT_NAME={config.get('recipientName', 'toi')}

# Planification
SCHEDULE_TIME={config.get('scheduleTime', '06:00')}
MAX_PER_FEED={config.get('maxPerFeed', '5')}

# Flux RSS (séparés par des virgules)
RSS_FEEDS={config.get('rssFeeds', '')}

# Podcasts Spotify (IDs séparés par des virgules)
PODCASTS_FEEDS={config.get('podcastsFeeds', '')}
SPOTIFY_CLIENT_ID={config.get('spotifyClientId', '')}
SPOTIFY_CLIENT_SECRET={config.get('spotifyClientSecret', '')}
"""

class ConfigHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        web_root = get_web_root()
        self.directory = web_root
        super().__init__(*args, directory=self.directory, **kwargs)
    
    def log_message(self, format, *args):
        # Mettre à jour l'activité à chaque requête
        global last_activity
        last_activity = datetime.now()
        
        # Afficher seulement les requêtes importantes (pas les favicon, etc.)
        if self.path not in ['/favicon.ico', '/'] and not self.path.startswith('/static/'):
            print(f"📡 {self.address_string()} - {self.path}")
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/api/config':
            env_path = get_env_path()
            env_dict = parse_env_file(env_path)
            config = env_to_config(env_dict)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'config': config}).encode())
        elif self.path == '/api/keepalive':
            # Endpoint pour garder le serveur actif
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'alive'}).encode())
        else:
            # Servir les fichiers statiques
            try:
                super().do_GET()
            except Exception as e:
                print(f"❌ Erreur lors du service de {self.path}: {e}")
                self.send_error(404, "File not found")
    
    def do_POST(self):
        global should_shutdown
        
        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            config = json.loads(post_data.decode('utf-8'))
            
            env_path = get_env_path()
            env_content = config_to_env(config)
            
            try:
                os.makedirs(os.path.dirname(env_path), exist_ok=True)
                
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.write(env_content)
                
                print(f"\n✅ Configuration sauvegardée dans: {env_path}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                
                # Marquer pour arrêt
                should_shutdown = True
                print("🛑 Arrêt du serveur dans 3 secondes...")
                
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def monitor_activity():
    """Surveille l'inactivité pour arrêter le serveur automatiquement"""
    global last_activity, should_shutdown
    
    while not should_shutdown:
        time.sleep(5)  # Vérifier toutes les 5 secondes
        
        inactivity = (datetime.now() - last_activity).total_seconds()
        
        # Si aucune activité depuis le timeout, arrêter le serveur
        if inactivity > activity_timeout:
            print(f"\n⏰ Aucune activité depuis {activity_timeout} secondes")
            print("🛑 Arrêt automatique du serveur...")
            should_shutdown = True
            break

def main():
    global should_shutdown, last_activity
    
    web_dir = get_web_root()
    
    if not os.path.exists(web_dir):
        print("❌ Erreur: Aucun dossier de configuration web trouvé!")
        print("📁 Dossiers cherchés:")
        print(f"   - {os.path.join(get_base_path(), 'web_config')}")
        print(f"   - {os.path.join(get_base_path(), 'temp_config')}")
        if getattr(sys, 'frozen', False):
            print(f"   - {os.path.join(sys._MEIPASS, 'web_config')}")
            print(f"   - {os.path.join(sys._MEIPASS, 'temp_config')}")
        sys.exit(1)
    
    # Vérifier que index.html existe
    index_path = os.path.join(web_dir, 'index.html')
    if not os.path.exists(index_path):
        print(f"❌ Erreur: index.html non trouvé dans {web_dir}")
        sys.exit(1)
    
    env_path = get_env_path()
    
    print("╔════════════════════════════════════════════════╗")
    print("║   🚀 Interface de Configuration Newsletter    ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    print(f"📡 Serveur démarré sur http://localhost:{PORT}")
    print(f"📂 Dossier web: {web_dir}")
    print(f"📄 Fichier .env: {env_path}")
    print("🌐 Ouverture du navigateur...")
    print()
    print("💡 Le serveur s'arrêtera automatiquement après:")
    print(f"   - Sauvegarde de la configuration")
    print(f"   - {activity_timeout} secondes d'inactivité")
    print(f"   - Ctrl+C dans le terminal")
    print("═" * 50)
    
    # Afficher les fichiers disponibles
    print("📁 Fichiers disponibles:")
    for file in os.listdir(web_dir):
        print(f"   📄 {file}")
    print("═" * 50)
    
    # Démarrer le moniteur d'activité
    activity_monitor = threading.Thread(target=monitor_activity, daemon=True)
    activity_monitor.start()
    
    class ShutdownServer(socketserver.TCPServer):
        allow_reuse_address = True
        timeout = 1
        
        def service_actions(self):
            """Vérifie périodiquement si on doit arrêter le serveur"""
            if should_shutdown:
                print("\n👋 Arrêt du serveur en cours...")
                self.shutdown()
    
    try:
        with ShutdownServer(("", PORT), ConfigHandler) as httpd:
            # Ouvrir le navigateur
            webbrowser.open(f'http://localhost:{PORT}')
            
            print(f"🎯 Serveur prêt! Accédez à http://localhost:{PORT}")
            print("⏳ En attente de connexions...")
            
            # Servir avec timeout pour permettre la vérification régulière
            while not should_shutdown:
                httpd.handle_request()
                
    except KeyboardInterrupt:
        print("\n👋 Interruption clavier détectée")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
    finally:
        print("✅ Serveur arrêté avec succès!")

if __name__ == "__main__":
    main()