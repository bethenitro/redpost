# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include SSL certificates
        ('venv/Lib/site-packages/certifi/cacert.pem', 'certifi'),
    ],
    hiddenimports=[
        'praw',
        'prawcore',
        'prawcore.auth',
        'prawcore.const',
        'prawcore.exceptions',
        'prawcore.rate_limit',
        'prawcore.requestor',
        'prawcore.sessions',
        'requests',
        'requests.auth',
        'requests.packages.urllib3',
        'urllib3',
        'certifi',
        'websocket',
        'update_checker',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RedditBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)