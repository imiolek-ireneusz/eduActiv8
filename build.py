import shutil
import subprocess
from pathlib import Path
import sys

# === Configuration ===
SCRIPT_NAME = "eduactiv8.py"
PROJECT_NAME = "eduActiv8"
VERSION = "4.25.06"
ICON_PATH = Path("res/icon/eduactiv8.ico")
VERSION_FILE = Path("version.txt")
DIST_PATH = Path("dist")
BUILD_PATH = Path("build")
SPEC_FILE = Path(f"{PROJECT_NAME}.spec")

# === Clean previous builds ===
for path in [DIST_PATH, BUILD_PATH, SPEC_FILE]:
    if path.exists():
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)

# === Build PyInstaller command ===
command = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",
    "--hidden-import=sqlite3",
    "--hidden-import=json",
    "--hidden-import=xml.etree.ElementTree",
    f"--name={PROJECT_NAME}",
    f"--icon={ICON_PATH}",
    f"{SCRIPT_NAME}",
]

# Include version file if present
if VERSION_FILE.exists():
    command.append(f"--version-file={VERSION_FILE}")

print("Running PyInstaller...")
subprocess.run(command, check=True)
print(f"✅ Build complete! Find your app folder in: {DIST_PATH / PROJECT_NAME}")
