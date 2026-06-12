# Structure config.py et dépendances

## config.py — structure minimale obligatoire

```python
# config.py
APP_NAME: str = "NomApp"
APP_VERSION: str = "1.0.0"

# Base de données (si applicable)
DB_PATH: str = "data/nom_app.db"
DB_SCHEMA_VERSION: int = 1                    # voir @rules/db.md

# Préférences (si applicable) — fichier à la racine du projet
PREFERENCES_FILE: str = "preferences.json"

# Internationalisation (si activée) — voir @rules/i18n.md
DEFAULT_LOCALE: str = "fr"
SUPPORTED_LOCALES: list[str] = ["fr", "en"]

# Logging — voir @rules/logging.md
LOG_DIR: str = "logs"                         # ou %APPDATA%/[NomApp]/logs pour packaging
LOG_LEVEL: str = "INFO"
LOG_MAX_BYTES: int = 1_000_000                # 1 MB par fichier
LOG_BACKUP_COUNT: int = 5

# Couleurs primaires — remplacer ces 4 valeurs pour changer la couleur primaire
PRIMARY_50:  str = "#EEF2FF"   # fond sélection clair
PRIMARY_400: str = "#818CF8"   # texte actif sombre
PRIMARY_600: str = "#4F46E5"   # texte/bordure actif clair
PRIMARY_900: str = "#312E81"   # fond sélection sombre

# Icônes qtawesome — couleurs par thème (contrainte technique : non stylable via QSS)
ICON_COLORS: dict = {
    "light": {
        "default":  "#6B7280",   # text-subtle
        "active":   PRIMARY_600,
        "danger":   "#DC2626",   # danger-600
        "success":  "#16A34A",   # success-600
        "muted":    "#9CA3AF",   # text-muted
    },
    "dark": {
        "default":  "#9CA3AF",   # text-subtle sombre
        "active":   PRIMARY_400,
        "danger":   "#F87171",   # danger-600 sombre
        "success":  "#4ADE80",   # success-600 sombre
        "muted":    "#6B7280",   # text-muted sombre
    }
}
```

Toute constante réutilisée dans plus d'un fichier va dans `config.py`.

---

## Dérivation des tokens primaires à partir de `primary-600`

L'utilisateur fournit **uniquement** `primary-600` en Phase 1. Claude dérive les 3 autres
par règle déterministe basée sur HSL — même teinte (`H`), même saturation (`S`), seule
la luminosité (`L`) change.

| Token         | Formule HSL                                | Rôle visuel               |
| ------------- | ------------------------------------------ | ------------------------- |
| `primary-50`  | `H` inchangé · `S` inchangé · `L` = 95%    | Fond sélection (clair)    |
| `primary-400` | `H` inchangé · `S` inchangé · `L` = 70%    | Texte actif (sombre)      |
| `primary-600` | **Fourni par l'utilisateur**                | Texte/bordure actif (clair) |
| `primary-900` | `H` inchangé · `S` inchangé · `L` = 25%    | Fond sélection (sombre)   |

Méthode : convertir le hex `primary-600` en HSL, recalculer les 3 luminosités, reconvertir
en hex. Aucune dépendance externe — utiliser `colorsys` (stdlib) côté Claude.

### Table de correspondance des couleurs proposées par défaut

| Nom         | primary-600 | primary-50 (dérivé) | primary-400 (dérivé) | primary-900 (dérivé) |
| ----------- | ----------- | ------------------- | -------------------- | -------------------- |
| Slate Blue  | #4F46E5     | #EEF2FF             | #818CF8              | #312E81              |
| Royal Blue  | #2563EB     | #EFF6FF             | #60A5FA              | #1E3A8A              |
| Emerald     | #059669     | #ECFDF5             | #34D399              | #064E3B              |
| Crimson     | #DC2626     | #FEF2F2             | #F87171              | #7F1D1D              |
| Amber       | #D97706     | #FFFBEB             | #FBBF24              | #78350F              |
| Violet      | #7C3AED     | #F5F3FF             | #A78BFA              | #4C1D95              |

Pour toute valeur personnalisée (option E en Phase 1), Claude calcule les 3 dérivés et
les annonce explicitement avant de les écrire dans `config.py`.

---

## Préférences persistées — valeurs par défaut

Activées si Phase 1 Q3 = Oui. Stockées dans `preferences.json` à la **racine du projet**
(gitignoré). En mode packaging `.exe`, déplacer vers `%APPDATA%/[NomApp]/preferences.json`.

| Préférence         | Valeur par défaut |
| ------------------ | ----------------- |
| thème              | système OS        |
| fenêtre taille     | 1280×800          |
| fenêtre position   | centrée           |
| drawer état        | fermé             |
| langue (si i18n)   | fr                |

Lecture/écriture via `utils/helpers.py` (fonctions pures, voir `@rules/mvc.md`).

---

## requirements.txt — versioning loose

```
PyQt6>=6.7.0
qtawesome>=1.3.0
```

Versions loose (`>=`), fixées à la version minimale validée en Phase 1.

### Dépendances conditionnelles

| Condition Phase 1                    | Dépendance ajoutée à requirements.txt   |
| ------------------------------------ | --------------------------------------- |
| DB = SQLite                          | aucune (sqlite3 stdlib)                 |
| DB = PostgreSQL                      | `psycopg[binary]>=3.2.0`                |
| DB = JSON ou CSV                     | aucune                                  |
| i18n = Oui                           | aucune (PyQt6.QtCore.QTranslator natif) |

---

## requirements-dev.txt — si tests activés OU pour usage pro

```
pytest>=8.0.0
pytest-qt>=4.4.0
ruff>=0.6.0
mypy>=1.11.0
```

Installation locale :

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Voir `@rules/tests.md` pour la structure des tests.

---

## pyproject.toml — configuration outillage

Livré dans le dernier lot applicatif :

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]
ignore = []

[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true
exclude = ["tests/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
qt_api = "pyqt6"
```

Commandes développeur :

```bash
ruff check .              # lint
ruff format .             # format
mypy .                    # type-check
pytest                    # tests
```

---

## Internationalisation (si activée)

Synthèse — détail complet dans `@rules/i18n.md`.

- Toutes les chaînes visibles passent par `self.tr("texte")` dans les Views.
- Fichiers dans `resources/i18n/` : `app_fr.ts` et `app_en.ts`, compilés en `.qm`.
- Langue chargée au démarrage depuis préférences, FR par défaut.
- Changement de langue : redémarrage (pas de rechargement à chaud).
- Zéro chaîne en dur dans Views, Controllers ou Models.

---

## Logging

Synthèse — détail complet dans `@rules/logging.md`.

- Module `logging` (stdlib) + `RotatingFileHandler`.
- Fichier `logs/[NomApp].log`, rotation à 1 MB × 5 backups.
- Niveau `INFO` par défaut, `DEBUG` si variable d'environnement `[NOM_APP]_DEBUG=1`.
- Format : `%(asctime)s [%(levelname)s] %(name)s — %(message)s`.

---

## Gestion des erreurs non capturées

Synthèse — détail dans `@rules/errors.md`.

- `sys.excepthook` installé dans `main.py` : log l'exception puis affiche un toast danger.
- Aucune trace dans stdout/stderr en mode `--windowed` (PyInstaller).

---

## Packaging Windows (.exe) — opt-in via Phase 1 Q6

Si Q6 = Oui, un dernier mini-lot livre `build.spec` + script `build.ps1`.

```bash
pyinstaller --onefile --windowed --name [NomApp] main.py ^
            --add-data "resources;resources" ^
            --icon resources/icon.ico
```

Détails :
- Chemins resources gérés via `helpers.resource_path()` qui résout `sys._MEIPASS` en mode bundled.
- `preferences.json` et `logs/` déplacés vers `%APPDATA%/[NomApp]/` en mode bundled.
- `build.spec` est **commité** (cf. `.gitignore` mis à jour).
- Signature `.exe` : hors périmètre du générateur (à faire à part avec `signtool`).
