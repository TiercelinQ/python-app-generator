# config.py structure and dependencies

## config.py — mandatory minimum structure

```python
# config.py
APP_NAME: str = "AppName"
APP_VERSION: str = "1.0.0"

# Database (if applicable)
DB_PATH: str = "data/app_name.db"
DB_SCHEMA_VERSION: int = 1                    # see @rules/db.md

# Preferences (if applicable) — file at the project root
PREFERENCES_FILE: str = "preferences.json"

# Internationalization (if enabled) — see @rules/i18n.md
DEFAULT_LOCALE: str = "fr"
SUPPORTED_LOCALES: list[str] = ["fr", "en"]

# Logging — see @rules/logging.md
LOG_DIR: str = "logs"                         # or %APPDATA%/[AppName]/logs for packaging
LOG_LEVEL: str = "INFO"
LOG_MAX_BYTES: int = 1_000_000                # 1 MB per file
LOG_BACKUP_COUNT: int = 5

# Toast position — see @layout.md
TOAST_POSITION: str = "top-right"

# Primary colors — replace these values to change the primary color
PRIMARY_50:  str = "#EEF2FF"   # light selection bg
PRIMARY_400: str = "#818CF8"   # dark active text
PRIMARY_600: str = "#4F46E5"   # light active text/border, primary button bg
PRIMARY_700: str = "#4338CA"   # primary button hover (both modes)
PRIMARY_800: str = "#3730A3"   # primary button pressed (both modes)
PRIMARY_900: str = "#312E81"   # dark selection bg

# qtawesome icon colors — per-theme (technical constraint: not styleable via QSS)
ICON_COLORS: dict = {
    "light": {
        "default":  "#6B7280",   # text-subtle
        "active":   PRIMARY_600,
        "success":  "#16A34A",   # success-600
        "warning":  "#D97706",   # warning-600
        "danger":   "#DC2626",   # danger-600
        "info":     "#2563EB",   # info-600
        "muted":    "#9CA3AF",   # text-muted
    },
    "dark": {
        "default":  "#9CA3AF",   # text-subtle dark
        "active":   PRIMARY_400,
        "success":  "#4ADE80",   # success-600 dark
        "warning":  "#FCD34D",   # warning-600 dark
        "danger":   "#F87171",   # danger-600 dark
        "info":     "#60A5FA",   # info-600 dark
        "muted":    "#6B7280",   # text-muted dark
    }
}
```

Any constant reused in more than one file goes into `config.py`.

---

## Deriving the primary tokens from `primary-600`

The user provides **only** `primary-600` in Phase 1. Claude derives the other 5 by a deterministic HSL-based rule — same hue (`H`), same saturation (`S`), only lightness (`L`) changes.

| Token         | HSL formula                                | Visual role               |
| ------------- | ------------------------------------------ | ------------------------- |
| `primary-50`  | `H` unchanged · `S` unchanged · `L` = 95%  | Selection bg (light)      |
| `primary-400` | `H` unchanged · `S` unchanged · `L` = 70%  | Active text (dark)        |
| `primary-600` | **Provided by the user**                    | Active text/border (light) |
| `primary-700` | `H` unchanged · `S` unchanged · `L` = 50%  | Primary button hover      |
| `primary-800` | `H` unchanged · `S` unchanged · `L` = 42%  | Primary button pressed    |
| `primary-900` | `H` unchanged · `S` unchanged · `L` = 25%  | Selection bg (dark)       |

Method: convert the `primary-600` hex to HSL, recompute the 5 lightnesses, convert back to hex. No external dependency — use `colorsys` (stdlib) on Claude's side. The derived `-700`/`-800` may differ by a few units from the reference values below (rounding); the reference values win when a preset name is chosen.

### Default proposed colors correspondence table

| Name        | primary-600 | primary-50 | primary-400 | primary-700 | primary-800 | primary-900 |
| ----------- | ----------- | ---------- | ----------- | ----------- | ----------- | ----------- |
| Slate Blue  | #4F46E5     | #EEF2FF    | #818CF8     | #4338CA     | #3730A3     | #312E81     |
| Royal Blue  | #2563EB     | #EFF6FF    | #60A5FA     | #1D4ED8     | #1E40AF     | #1E3A8A     |
| Emerald     | #059669     | #ECFDF5    | #34D399     | #047857     | #065F46     | #064E3B     |
| Crimson     | #DC2626     | #FEF2F2    | #F87171     | #B91C1C     | #991B1B     | #7F1D1D     |
| Amber       | #D97706     | #FFFBEB    | #FBBF24     | #B45309     | #92400E     | #78350F     |
| Violet      | #7C3AED     | #F5F3FF    | #A78BFA     | #6D28D9     | #5B21B6     | #4C1D95     |

For any custom value (option E in Phase 1), Claude computes the 5 derived values and announces them explicitly before writing them to `config.py`.

---

## Persisted preferences — default values

Enabled if Phase 1 Q3 = Yes. Stored in `preferences.json` at the **project root** (gitignored). In `.exe` packaging mode, move to `%APPDATA%/[AppName]/preferences.json`.

| Preference         | Default value     |
| ------------------ | ----------------- |
| theme              | OS system         |
| window size        | 1280×800          |
| window position    | centered          |
| drawer state       | closed            |
| language (if i18n) | fr                |

Read/write via `utils/helpers.py` (pure functions, see `@rules/mvc.md`).

---

## requirements.txt — loose versioning

```
PyQt6>=6.7.0
qtawesome>=1.3.0
```

Loose versions (`>=`), pinned to the minimum version validated in Phase 1.

### Conditional dependencies

| Phase 1 condition                    | Dependency added to requirements.txt    |
| ------------------------------------ | --------------------------------------- |
| DB = SQLite                          | none (sqlite3 stdlib)                   |
| DB = PostgreSQL                      | `psycopg[binary]>=3.2.0`                |
| DB = JSON or CSV                     | none                                    |
| i18n = Yes                           | none (PyQt6.QtCore.QTranslator native)  |

> **Version maintenance**: these versions reflect the state validated at the time of writing. Before pinning in a new project, re-confirm the current minimum versions (`pip index versions`, PyPI). The loose-version rule and the structure stay; the numbers are refreshed per project in Phase 1.

---

## requirements-dev.txt — if tests enabled OR for pro use

```
pytest>=8.0.0
pytest-qt>=4.4.0
ruff>=0.6.0
mypy>=1.11.0
```

Local install:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

See `@rules/tests.md` for the test structure.

---

## pyproject.toml — tooling configuration

Delivered in the last application batch:

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

Developer commands:

```bash
ruff check .              # lint
ruff format .             # format
mypy .                    # type-check
pytest                    # tests
```

---

## Internationalization (if enabled)

Summary — full detail in `@rules/i18n.md`.

- All visible strings go through `self.tr("text")` in the Views.
- Files in `resources/i18n/`: `app_fr.ts` and `app_en.ts`, compiled to `.qm`.
- Language loaded at startup from preferences, FR by default.
- Language change: restart (no hot reload).
- Zero hardcoded string in Views, Controllers, or Models.

---

## Logging

Summary — full detail in `@rules/logging.md`.

- `logging` module (stdlib) + `RotatingFileHandler`.
- File `logs/[AppName].log`, rotation at 1 MB × 5 backups.
- `INFO` level by default, `DEBUG` if env var `[APP_NAME]_DEBUG=1`.
- Format: `%(asctime)s [%(levelname)s] %(name)s — %(message)s`.

---

## Uncaught error handling

Summary — detail in `@rules/errors.md`.

- `sys.excepthook` installed in `main.py`: logs the exception then shows a danger toast.
- No trace to stdout/stderr in `--windowed` mode (PyInstaller).

---

## Windows packaging (.exe) — opt-in via Phase 1 Q6

If Q6 = Yes, a final mini-batch delivers `build.spec` + a `build.ps1` script.

```bash
pyinstaller --onefile --windowed --name [AppName] main.py ^
            --add-data "resources;resources" ^
            --icon resources/icon.ico
```

Details:
- Resource paths handled via `helpers.resource_path()` which resolves `sys._MEIPASS` in bundled mode.
- `preferences.json` and `logs/` moved to `%APPDATA%/[AppName]/` in bundled mode.
- `build.spec` is **committed** (cf. updated `.gitignore`).
- `.exe` signing: out of the generator's scope (done separately with `signtool`).
