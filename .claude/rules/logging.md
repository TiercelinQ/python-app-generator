# Logging rules

## Principle

- `logging` module (stdlib) only — zero external dependency.
- `RotatingFileHandler` to cap log size.
- One logger instance per module: `logger = logging.getLogger(__name__)`.
- Zero `print()` in delivered code — only `logger.*`.

---

## Centralized configuration

Mandatory file `utils/logger.py` (pure function, imported by `main.py`):

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

## Usage in modules

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

### Level conventions

| Level    | Usage                                                                  |
| -------- | ---------------------------------------------------------------------- |
| DEBUG    | Detailed traces, intermediate values                                   |
| INFO     | Important business steps (startup, login, key user action)             |
| WARNING  | Unexpected but non-blocking conditions (user validation failed)        |
| ERROR    | Intercepted business error (DatabaseError, FileError…)                 |
| CRITICAL | Imminent crash / corrupt state — precedes sys.exit                     |

### `logger.exception` mandatory

In `except` blocks that re-raise or fail silently (toast shown), use `logger.exception(message)` to capture the full stacktrace.

---

## Activation from main.py

```python
# main.py
from utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Démarrage application")
```

---

## Anti-patterns — what NOT to do

- **Do not** use `print()` in delivered code — only `logger.*`.
- **Do not** log a password, token, or personally identifiable data.
- **Do not** write to stdout in `--windowed` mode (PyInstaller).
- **Do not** silence an `except` that doesn't re-raise without a `logger.exception(...)`.
- **Do not** configure logging outside `utils/logger.py` (single setup point, called first in `main.py`).

## Integrity verification

Detailed in `@rules/verification.md`. Key points: `utils/logger.py` present and conforming; `setup_logging()` called on the first line of `main.py` (before any business import); no `print(` in `models/`, `views/`, `controllers/`, `utils/`; every non-re-raising `except` calls `logger.exception(...)`.
