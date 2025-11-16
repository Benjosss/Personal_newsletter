# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Répertoire racine du projet
project_root = Path(__name__).parent.absolute()

# Ajouter le répertoire racine au path Python
sys.path.insert(0, str(project_root))

block_cipher = None

a = Analysis(
    ['config.py'],  # Fichier principal à packager
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Inclure le dossier web_config
        (str(project_root / 'web_config'), 'web_config'),
        # Inclure le dossier temp_config
        (str(project_root / 'temp_config'), 'temp_config'),
        # Inclure le fichier .env.example
        (str(project_root / '.env.example'), '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Options pour un seul fichier
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='newsletter_config',  # Nom de l'exécutable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Pas de console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)