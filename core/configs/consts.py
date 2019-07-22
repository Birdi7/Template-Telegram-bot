"""
This file is created for config which is not depends on a particular project
and you won't need to specify them, but vars from here are used in other configs
"""
from pathlib import Path

BASE_DIR: Path = Path('.').parent.parent
LOGS_FOLDER: Path = BASE_DIR / "logs"
