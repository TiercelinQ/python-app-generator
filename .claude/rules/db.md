# Règles base de données

## Stack par choix Phase 1 Q2

| Choix DB    | Bibliothèque             | Fichier modèle de référence |
| ----------- | ------------------------ | --------------------------- |
| SQLite      | `sqlite3` (stdlib)       | `models/db.py`              |
| PostgreSQL  | `psycopg[binary]>=3.2.0` | `models/db.py`              |
| JSON        | `json` (stdlib)          | direct dans les modèles     |
| CSV         | `csv` (stdlib)           | direct dans les modèles     |
| aucune      | —                        | —                           |

---

## Architecture (SQLite / PostgreSQL)

### `models/db.py` — point d'accès unique

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

### Usage dans les modèles métier

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

## Migrations versionnées (SQLite / PostgreSQL)

### Principe

- Le schéma est versionné via une table `_schema_version` (entier).
- `config.DB_SCHEMA_VERSION` indique la version cible attendue par le code.
- Au démarrage, `models/migrations.py` compare `version_en_db` et `version_cible`,
  applique séquentiellement les migrations manquantes.
- **Une seule direction** : `up` uniquement. Pas de rollback automatique.

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

### Appel depuis main.py

```python
from models.migrations import run_migrations

setup_logging()
run_migrations()   # avant création de la MainWindow
```

---

## Mode JSON / CSV (projets sans SGBD)

- Stockage dans `data/` à la racine du projet (gitignoré).
- `utils/helpers.py` expose `load_json(path)` / `save_json(path, data)` /
  `read_csv(path)` / `write_csv(path, rows)`.
- Chaque modèle métier encapsule son chemin de fichier.
- Pas de migrations versionnées en JSON/CSV — la responsabilité incombe à l'utilisateur.
- En cas de schéma JSON modifié : conversion explicite au chargement (fonction dédiée).

---

## Interdictions

- Zéro requête SQL en dehors de `models/`.
- Zéro accès direct à `sqlite3.connect()` hors `models/db.py`.
- Zéro `SELECT *` sans justification (lister les colonnes).
- Zéro concaténation de chaîne pour construire des requêtes — uniquement paramètres `?` ou `%s`.
- Zéro migration `down` automatique.

---

## Vérification d'intégrité

1. Si DB ≠ aucune : `models/db.py` présent avec `get_connection` context manager.
2. Si DB ≠ aucune : `models/migrations.py` présent et appelé dans `main.py` avant la MainWindow.
3. `config.DB_SCHEMA_VERSION` cohérent avec le max(MIGRATIONS.keys()).
4. Aucun `sqlite3.connect` ni `psycopg.connect` hors `models/db.py`.
5. Tous les paramètres SQL passent via paramètres préparés (`?` ou `%s`), jamais en concaténation.
