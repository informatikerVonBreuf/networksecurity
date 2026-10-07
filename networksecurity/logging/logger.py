"""Écrire les journaux du pipeline dans la console et dans un fichier."""

import logging
from datetime import datetime
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            Path("logs") / f"{datetime.now():%Y%m%d_%H%M%S_%f}.log", encoding="utf-8"
        ),
    ],
)
