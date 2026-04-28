import os
import hashlib

EXCLUDE_PATTERNS = [
    ".git",
    "init-db",
    "backups",
    "__pycache__",
    "db",
    "logs",
    ".DS_Store",
]

def get_addons_dir():
    current_file = os.path.abspath(__file__)

    models_dir = os.path.dirname(current_file)
    nosheet_dir = os.path.dirname(models_dir)
    addons_dir = os.path.dirname(nosheet_dir)

    return addons_dir

ADDONS_DIR = get_addons_dir()

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def is_excluded(path):
    return any(x in path for x in EXCLUDE_PATTERNS)

def scan_files():
    for root, _, files in os.walk(ADDONS_DIR):
        for f in files:
            path = os.path.join(root, f)

            if is_excluded(path):
                continue

            yield path

def build_hash_map():
    result = {}
    for path in scan_files():
        try:
            result[path] = hash_file(path)
        except Exception:
            pass
    return result
