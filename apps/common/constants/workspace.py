import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
WORKSPACE_DIR = BASE_DIR / 'workspace'

os.makedirs(WORKSPACE_DIR, exist_ok=True)