# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_game_pyinstall_ver.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/background.jpg', 'assets'), ('assets/select2.png', 'assets'), ('assets/Quit Rect.png', 'assets'), ('assets/peace_pic.jpg', 'assets'), ('assets/space.png', 'assets'), ('assets/ship.png', 'assets'), ('assets/bang.png', 'assets'), ('assets/Quit_Button.png', 'assets'), ('score_record.db', '.'), ('sounds/game_ready.mp3', 'sounds'), ('sounds/game_start.mp3', 'sounds'), ('sounds/main_touch.mp3', 'sounds'), ('sounds/game_touch.mp3', 'sounds'), ('sounds/react_end.mp3', 'sounds'), ('sounds/remem_correct.mp3', 'sounds'), ('sounds/remem_incorrect.mp3', 'sounds'), ('sounds/remem_end.mp3', 'sounds'), ('sounds/space_bang.mp3', 'sounds'), ('sounds/space_start.mp3', 'sounds'), ('sounds/space_end.mp3', 'sounds'), ('sounds/space_bg.mp3', 'sounds')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main_game_pyinstall_ver',
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
