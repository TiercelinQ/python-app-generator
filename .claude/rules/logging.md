# Règles logging

## Principe

- Module `logging` (stdlib) uniquement — zéro dépendance externe.
- `RotatingFileHandler` pour limiter la taille des logs.
- Une instance logger par module : `logger = logging.getLogger(__name__)`.
- Zéro `print()` dans le code livré — uniquement `logger.*`.

---

## Configuration centralisée

Fichier obligatoire `utils/logger.py` (fonction pure, importée par `main.py`) :

```python
"""Configuration centralisée du logging."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import config


def setup_logging() -> None:
    """Configure le logging applicatif."""
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{config.APP_NAME.lower()}.log"

    level = logging.DEBUG if _debug_enabled() else getattr(logging, config.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(file_handler)

    # En mode debug ou hors --windowed : écho console
    if _debug_enabled() and sys.stderr is not None:
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(formatter)
        console.setLevel(logging.DEBUG)
        root.addHandler(console)


def _debug_enabled() -> bool:
    import os
    return os.environ.get(f"{config.APP_NAME.upper()}_DEBUG") == "1"
```

---

## Usage dans les modules

```python
# models/client_model.py
import logging

logger = logging.getLogger(__name__)


class ClientModel:
    def save(self, data: dict) -> None:
        logger.debug("Sauvegarde client : %s", data)
        try:
            ...
        except DatabaseError:
            logger.exception("Échec sauvegarde client")
            raise
```

### Conventions de niveaux

| Niveau   | Usage                                                                  |
| -------- | ---------------------------------------------------------------------- |
| DEBUG    | Traces détaillées, valeurs intermédiaires                              |
| INFO     | Étapes métier importantes (démarrage, login, action utilisateur clé)   |
| WARNING  | Conditions inattendues mais non bloquantes (validation utilisateur KO) |
| ERROR    | Erreur métier interceptée (DatabaseError, FileError…)                  |
| CRITICAL | Crash imminent / état corrompu — précède sys.exit                      |

### `logger.exception` obligatoire

Dans les blocs `except` qui re-raise ou échouent silencieusement (toast affiché),
utiliser `logger.exception(message)` pour capturer la stacktrace complète.

---

## Activation depuis main.py

```python
# main.py
from utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Démarrage application")
```

---

## Interdictions

- Zéro `print()` dans le code livré.
- Zéro log de mot de passe, token, donnée personnelle identifiable.
- Pas d'écriture vers stdout en mode `--windowed` (PyInstaller).

---

## Vérification d'intégrité

1. `utils/logger.py` présent et conforme au template.
2. `setup_logging()` appelé en première ligne de `main.py` (avant tout autre import métier).
3. Aucun `print(` dans `models/`, `views/`, `controllers/`, `utils/`.
4. Tous les blocs `except` qui ne re-raise pas appellent `logger.exception(...)`.
