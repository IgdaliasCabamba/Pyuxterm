# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

hidden_libs = [
        
        "src.uterm",
        "src.urequirements",
        "src.static_files",
        "_system",
        "server",
        "main",

        "aiohttp",
        "aiohttp_jinja2",
        "aiosignal",
        "altgraph",
        "async_timeout",
        "attrs",
        "bidict",
        "certifi",
        "charset_normalizer",
        "click",
        "engineio",
        "frozenlist",
        "hjson",
        "idna",
        "importlib_metadata",
        "multidict",
        "socketio",
        "requests",
        "urllib3",
        "yarl",
        "zipp",
        
        "engineio.async_drivers.aiohttp",
        "engineio.async_aiohttp"
    ]

app_resources = [
    ( 'app/static', 'static' ),
    ( 'app/templates', 'templates'),
    ( 'app/settings', 'settings'),
]

a = Analysis(
    ['app/__main__.py'],
    pathex=[],
    binaries=[],
    datas=app_resources,
    hiddenimports=hidden_libs,
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
    name='pyuxterm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
