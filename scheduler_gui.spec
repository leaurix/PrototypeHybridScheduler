# scheduler_gui.spec
# PyInstaller spec — double-click build.bat to compile

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['scheduler_gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('dummy_dataset', 'dummy_dataset'),          # bundle the CSV dataset
        ('hybrid_scheduler', 'hybrid_scheduler'),    # bundle all source modules
    ],
    hiddenimports=(
        collect_submodules('ortools') +
        collect_submodules('hybrid_scheduler') +
        ['tkinter', 'tkinter.ttk', 'pandas', 'ast']
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['run_demo'],          # drop run_demo.py from the bundle
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
    name='HybridScheduler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # no black terminal window behind the GUI
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # swap in an .ico path here if you have one
)
