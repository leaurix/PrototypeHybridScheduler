# scheduler_gui.spec
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs

block_cipher = None

ortools_hidden   = collect_submodules('ortools')
ortools_datas    = collect_data_files('ortools')
ortools_binaries = collect_dynamic_libs('ortools')

a = Analysis(
    ['scheduler_gui.py'],
    pathex=['.'],
    binaries=ortools_binaries,
    datas=[
        ('dummy_dataset', 'dummy_dataset'),
        ('real_dataset',  'real_dataset'),
        ('hybrid_scheduler', 'hybrid_scheduler'),
    ] + ortools_datas,
    hiddenimports=(
        ortools_hidden +
        collect_submodules('hybrid_scheduler') +
        collect_submodules('openpyxl') +
        [
            'tkinter', 'tkinter.ttk', 'pandas', 'ast',
            'openpyxl', 'openpyxl.styles', 'openpyxl.utils',
            'openpyxl.styles.fills', 'openpyxl.styles.fonts',
            'openpyxl.styles.alignment', 'openpyxl.styles.borders',
            'ortools.sat.python.cp_model',
            'ortools.sat.python.cp_model_helper',
            'ortools.constraint_solver.pywrapcp',
        ]
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['run_demo'],
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
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
