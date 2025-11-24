# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['rumps', 'pystray', 'PIL', 'pkg_resources'],
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
    name='WTWOW-KillSwitch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS specific
app = BUNDLE(
    exe,
    name='WTWOW-KillSwitch.app',
    icon=None,
    bundle_identifier='com.wtwow.killswitch',
    info_plist={
        'LSUIElement': True,
        'CFBundleName': 'WTWOW-KillSwitch',
        'CFBundleDisplayName': 'WTWOW KillSwitch',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True
    },
)
