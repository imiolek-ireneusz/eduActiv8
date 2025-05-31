# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

def collect_data_files():
    datas = []
    resource_dirs = ["classes", "game_boards", "i18n", "locale"]  # "res", "xml"
    exclude_dirs = {"dist", "build"}

    for folder in resource_dirs:
        folder_path = Path(folder)
        if not folder_path.exists():
            continue
        # Skip if folder is in exclude list
        if folder_path.name in exclude_dirs:
            continue

        for file_path in folder_path.rglob("*"):
            if file_path.is_file():
                # Skip any files inside excluded folders just in case
                if any(part in exclude_dirs for part in file_path.parts):
                    continue
                target_dir = str(file_path.parent)
                datas.append((str(file_path), target_dir))

    return datas


datas = collect_data_files()

#from PyInstaller.utils.hooks import collect_data_files
#from pathlib import Path

# Existing collected data files (e.g., from your resource dirs)
# datas = collect_data_files("classes")  # example, replace with your actual data gathering code

# Add individual files explicitly
extra_files = [
    ("CHANGES.txt", "."),    
    ("CREDITS.txt", "."),
    ("LICENSE", "."),
    ("README.md", "."),
    ("README.txt", "."),
    ("bin/espeak.exe", "bin")
]

# Convert to PyInstaller's format: list of (src_path, dest_path)
extra_datas = [(str(Path(f[0]).resolve()), f[1]) for f in extra_files]

# Combine all datas
datas += extra_datas


a = Analysis(
    ['eduactiv8.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'sqlite3',
        'json',
        'xml.etree.ElementTree',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'scipy', 'site', 'tornado', 'PIL', 'PyQt4', 'PyQt5', 'pydoc', 'pythoncom', 'pytz', 'pywintypes', 'pyz', 'pandas', 'sklearn', 'scapy', 'scrapy', 'sympy', 'kivy', 'pyramid', 'opencv', 'tensorflow', 'pipenv', 'pattern', 'mechanize', 'beautifulsoup4', 'requests', 'wxPython', 'pygi', 'pillow', 'pyglet', 'flask', 'django', 'pylint', 'pytube', 'odfpy', 'mccabe', 'pilkit', 'six', 'wrapt', 'astroid', 'isort'
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    icon='res/icon/eduactiv8.ico',
    version='version.txt',
    name='eduActiv8',
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
