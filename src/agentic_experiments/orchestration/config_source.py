from pathlib import Path
from typing import Final

SRC_PATH: Final[Path] = Path(__file__).parent.parent.parent.resolve()
PROJECT_PATH: Final[Path] = SRC_PATH.parent.resolve()

CONFIG_FOLDER: Final[Path] = Path(PROJECT_PATH, "config")
DOTENV_FILE_PATH: Final[Path] = Path(CONFIG_FOLDER, ".env")
