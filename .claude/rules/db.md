# Database rules

## Stack per Phase 1 Q2 choice

| DB choice   | Library                  | Reference model file        |
| ----------- | ------------------------ | --------------------------- |
| SQLite      | `sqlite3` (stdlib)       | `models/db.py`              |
| PostgreSQL  | `psycopg[binary]>=3.2.0` | `models/db.py`              |
| JSON        | `json` (stdlib)          | direct in the models        |
| CSV         | `csv` (stdlib)           | direct in the models        |
| none        | —                        | —                           |

---

## Architecture (SQLite / PostgreSQL)

### `models/db.py` — single access point

```python
"""Accès base de données — point d'entrée unique."""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import config
from models.exceptions import DatabaseError

logger = logging.getLogger(__name__)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Fournit une connexion SQLite avec foreign keys activées."""
    Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        logger.exception("Erreur SQLite")
        raise DatabaseError(str(e)) from e
    finally:
        conn.close()
```

### Usage in the business models

```python
# models/client_model.py
from models.db import get_connection


class ClientModel:
    def save(self, client: dict) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO clients (nom, email) VALUES (?, ?)",
                (client["nom"], client["email"]),
            )
            return cursor.lastrowid
```

---

## Versioned migrations (SQLite / PostgreSQL)

### Principle

- The schema is versioned via a `_schema_version` table (integer).
- `config.DB_SCHEMA_VERSION` indicates the target version expected by the code.
- At startup, `models/migrations.py` compares `db_version` and `target_version`, applies the missing migrations sequentially.
- **One direction only**: `up` only. No automatic rollback.

### `models/migrations.py`

```python
"""Migrations de schéma — appliquées au démarrage."""

import logging

import config
from models.db import get_connection
from models.exceptions import DatabaseError

logger = logging.getLogger(__name__)


MIGRATIONS: dict[int, list[str]] = {
    1: [
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        """,
    ],
    # 2: [ "ALTER TABLE clients ADD COLUMN telephone TEXT" ],
}


def run_migrations() -> None:
    """Applique toutes les migrations manquantes pour atteindre DB_SCHEMA_VERSION."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS _schema_version (version INTEGER NOT NULL)
        """)
        row = conn.execute("SELECT version FROM _schema_version LIMIT 1").fetchone()
        current = row["version"] if row else 0

        if current > config.DB_SCHEMA_VERSION:
            raise DatabaseError(
                f"Base en version {current}, code attend {config.DB_SCHEMA_VERSION}. "
                "Mise à jour de l'application requise."
            )

        for version in sorted(MIGRATIONS.keys()):
            if version > current:
                logger.info("Migration vers version %d", version)
                for statement in MIGRATIONS[version]:
                    conn.execute(statement)
                conn.execute("DELETE FROM _schema_version")
                conn.execute("INSERT INTO _schema_version (version) VALUES (?)", (version,))
                current = version
```

### Call from main.py

```python
from models.migrations import run_migrations

setup_logging()
run_migrations()   # avant création de la MainWindow
```

---

## JSON / CSV mode (projects without a DBMS)

- Storage in `data/` at the project root (gitignored).
- `utils/helpers.py` exposes `load_json(path)` / `save_json(path, data)` / `read_csv(path)` / `write_csv(path, rows)`.
- Each business model encapsulates its file path.
- No versioned migrations in JSON/CSV — responsibility lies with the user.
- If the JSON schema changes: explicit conversion at load time (dedicated function).

---

## Seed data (if DB ≠ none)

Delivered in the last phase of generation as a standalone script `scripts/seed.py`:
- Single responsibility: populate the DB with a coherent demo dataset via the business models (`models/`), never raw SQL outside `models/db.py`.
- Idempotent: check the target tables are empty before inserting; re-running must not duplicate rows.
- FK integrity: insert parents before children, reuse the returned ids.
- Volume: ~5-15 rows per entity, realistic French values.
- Never run automatically (no call from `main.py`); run manually with `python scripts/seed.py`.

---

## Anti-patterns — what NOT to do

- **Do not** write a SQL query outside `models/`.
- **Do not** call `sqlite3.connect()` / `psycopg.connect()` outside `models/db.py`.
- **Do not** `SELECT *` without justification (list the columns).
- **Do not** build a query by string concatenation — only `?` or `%s` parameters.
- **Do not** write an automatic `down` migration.

## Integrity verification

Detailed in `@rules/verification.md`. Key points (if DB ≠ none): `models/db.py` present with the `get_connection` context manager; `models/migrations.py` present and called in `main.py` before the MainWindow; `config.DB_SCHEMA_VERSION` consistent with `max(MIGRATIONS.keys())`; no `connect` outside `models/db.py`; all SQL parameters via prepared params (`?` / `%s`), never concatenation.
