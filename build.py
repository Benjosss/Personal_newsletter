import os
import shutil
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Construit l'exécutable avec PyInstaller"""
    
    project_root = Path(__file__).parent.absolute()
    dist_dir = project_root / 'dist'
    spec_file = project_root / 'build.spec'
    icon_file = project_root / 'web_config/favicon.ico'
    
    print("🔨 Construction de l'exécutable à partir de config.py...")
    
    # Check config.py
    if not (project_root / 'config.py').exists():
        print("❌ Erreur: Le fichier config.py n'existe pas!")
        return False
    
    # Check icon
    if not icon_file.exists():
        print("⚠️  Attention: Fichier icon.ico non trouvé")
        print("💡 L'exécutable sera créé sans icône personnalisée")
        print(f"📁 Attendu: {icon_file}")
    else:
        print(f"✅ Icône trouvée: {icon_file}")

    # Check needed files
    web_config_dir = project_root / 'web_config'
    temp_config_dir = project_root / 'temp_config'
    
    required_dirs = [
        ('web_config', web_config_dir),
        ('temp_config', temp_config_dir)
    ]
    
    for dir_name, dir_path in required_dirs:
        if not dir_path.exists():
            print(f"❌ Erreur: Le dossier '{dir_name}' n'existe pas!")
            print(f"📁 Attendu: {dir_path}")
            return False
    
    # Check web_config
    web_config_files = ['index.html', 'app.js']
    missing_files = []
    for file in web_config_files:
        if not (web_config_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Attention: Fichiers manquants dans web_config/: {', '.join(missing_files)}")
    
    # Check temp_config/index.html file
    if not (temp_config_dir / 'index.html').exists():
        print("❌ Attention: Fichier index.html manquant dans temp_config/")
    
    print("📁 Structure vérifiée:")
    print(f"   ✓ config.py → Présent")
    print(f"   ✓ web_config/favicon.ico → {'Présent' if icon_file.exists() else 'Absent'}")
    print(f"   ✓ web_config/ → {len(list(web_config_dir.iterdir()))} fichiers")
    print(f"   ✓ temp_config/ → {len(list(temp_config_dir.iterdir()))} fichiers")
    
    # Execute PyInstaller
    try:
        print("🚀 Lancement de PyInstaller...")
        result = subprocess.run([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            str(spec_file)
        ], check=True, capture_output=True, text=True)
        
        print("✅ Construction terminée avec succès!")
        
        # mv .exe
        exe_source = dist_dir / 'newsletter_config.exe'
        exe_dest = project_root / 'newsletter_config.exe'
        
        if exe_source.exists():
            # Delete old .exe
            if exe_dest.exists():
                print("🗑️  Suppression de l'ancien exécutable...")
                exe_dest.unlink()
            
            # mv .exe
            print("📦 Déplacement de l'exécutable...")
            shutil.move(str(exe_source), str(exe_dest))
            print(f"✅ Exécutable créé: {exe_dest}")
            
            # Clean build et dist folders
            print("🧹 Nettoyage des dossiers temporaires...")
            shutil.rmtree(project_root / 'build', ignore_errors=True)
            shutil.rmtree(dist_dir, ignore_errors=True)
            print("✅ Dossiers temporaires nettoyés")

            if icon_file.exists():
                print("🎨 L'icône personnalisée a été appliquée")
            
            print("\n🎉 Construction terminée avec succès!")
            print("💡 Vous pouvez maintenant utiliser 'newsletter_config.exe'")
            
        else:
            print("❌ L'exécutable n'a pas été trouvé dans le dossier dist")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la construction: {e}")
        if e.stderr:
            print(f"📄 Détails de l'erreur:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if build_executable():
        sys.exit(0)
    else:
        sys.exit(1)