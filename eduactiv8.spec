# -*- mode: python -*-

import sys

p = sys.platform
block_cipher = None

# command: $ pyinstaller eduactiv8.spec

# hiddenimports=["_io", "pyimod03_importers", "colorsys", "_struct", "struct"],
if p == "linux" or p == "linux2":
    hidden_imports = ["_io", "pyimod03_importers", "colorsys", "_struct", "struct", "sqlite3", "ast", "xml.etree.ElementTree"]
else:
    hidden_imports = ["_io", "pyimod03_importers", "colorsys", "_struct", "struct"]

a = Analysis(['eduactiv8.py'],
             pathex=['/Users/cextested/Documents/eduActiv8/eduActiv8-3.70.823/dist/eduActiv8'],
             binaries=[],
             datas = [("CHANGES.txt", "."), ("CREDITS.txt", "."), ("LICENSE", "."), ("README.txt", "."), ("xml", "xml"),
                      ("locale", "locale"), ("res", "res"), ("classes", "classes"), ("game_boards", "game_boards"), ("i18n","i18n")],
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=["numpy", "scipy", 'matplotlib', 'PIL', 'cython', 'zmq'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if p == "linux" or p == "linux2":
    print("Building for Linux")
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='eduActiv8',
              debug=False,
              strip=False,
              upx=True,
              console=True,
              icon='res/icon/eduactiv8.ico')

elif p == "win32" or p == "cygwin":
    print("Building for Windows")
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='eduActiv8',
              debug=False,
              strip=False,
              upx=True,
              console=False,
              icon='res\icon\eduactiv8.ico')

elif p == "darwin":
    print("Building for Mac OS")
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='eduActiv8',
              debug=False,
              strip=False,
              upx=True,
              console=False,
              icon='res/icon/eduactiv8.icns')

    app = BUNDLE(exe,
                 name='eduActiv8.app',
                 icon='res/icon/eduactiv8.icns',
                 info_plist={
                             'NSHighResolutionCapable': 'True'
                 },
                 bundle_identifier="org.eduactiv8.eduactiv8")

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='eduActiv8')
