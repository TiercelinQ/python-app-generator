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

# Accent stops — derived from the palette accent (primary-600). Neutrals (bg/text/border)
# live in the QSS sheets, not here. See @rules/config.md "Deriving the full palette".
PRIMARY_50:  str = "#EDF3F8"   # light selection bg
PRIMARY_400: str = "#B3B3B3"   # dark active text (default palette: neutral grey accent)
PRIMARY_600: str = "#4682B4"   # light active text/border, light primary button bg
PRIMARY_700: str = "#396A93"   # light primary button hover
PRIMARY_800: str = "#2F5879"   # light primary button pressed
PRIMARY_900: str = "#404040"   # dark selection bg
ON_PRIMARY:  str = "#FFFFFF"   # text on light accent + danger buttons; dark primary button uses near-black (styles_dark.qss)

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
        "default":  "#939393",   # text-subtle dark
        "active":   PRIMARY_400,
        "success":  "#4A9E6A",   # success-600 dark
        "warning":  "#CCA840",   # warning-600 dark
        "danger":   "#C04A4A",   # danger-600 dark
        "info":     "#4682B4",   # info-600 dark
        "muted":    "#6E6E6E",   # text-muted dark
    }
}
```

Any constant reused in more than one file goes into `config.py`.

---

## Deriving the full palette

In Phase 1 the user picks a **named palette** or enters a **custom palette** = 5 **light** roles (fond principal → `bg`, fond secondaire → `bg-subtle`, accent → `primary-600`, texte → `text`, détails → `border`). Claude derives everything else — supporting light tokens, the 5 accent stops, the **whole dark theme**, and `onPrimary` — and writes literal hex into `styles_light.qss` / `styles_dark.qss` and `config.py`. Role→token mapping, neutral sRGB mixes, and dark lightness targets: `design-system.md §2`. After deriving, Claude runs the WCAG AA check (`§12` below) and reports any failure without blocking.

> The neutral tokens (`bg`, `bg-subtle`, `bg-muted`, `bg-elevated`, `text*`, `border*`) live **in the QSS sheets**, not in `config.py`; only the accent stops and `ICON_COLORS` live in `config.py`. The derivation populates both.
>
> Default-palette exception: its dark accent is a **neutral grey** (`#9E9E9E`), so the dark primary button (fill `#9E9E9E` / hover `#808080` / pressed `#6B6B6B`, near-black text) diverges from the light Steel Blue ramp. Those dark grey button values are written as literals in `styles_dark.qss` (like the dark neutrals); `config.py PRIMARY_600/700/800` keep the light ramp, while `PRIMARY_400`/`PRIMARY_900` (dark-only stops) already hold the grey active/selection values. For a custom palette the accent is a single hue and the `PRIMARY_*` stops stay consistent across both sheets.

### Accent stops — HSL rule from `primary-600`

The accent provides `primary-600`; Claude derives the other 5 by a deterministic HSL-based rule — same hue (`H`), same saturation (`S`), only lightness (`L`) changes.

| Token         | HSL formula                                | Visual role               |
| ------------- | ------------------------------------------ | ------------------------- |
| `primary-50`  | `H` unchanged · `S` unchanged · `L` = 95%  | Selection bg (light)      |
| `primary-400` | `H` unchanged · `S` unchanged · `L` = 70%  | Active text (dark)        |
| `primary-600` | **Provided by the user**                    | Active text/border (light) |
| `primary-700` | `H` unchanged · `S` unchanged · `L` = 50%  | Primary button hover      |
| `primary-800` | `H` unchanged · `S` unchanged · `L` = 42%  | Primary button pressed    |
| `primary-900` | `H` unchanged · `S` unchanged · `L` = 25%  | Selection bg (dark)       |

Method: convert the `primary-600` hex to HSL, recompute the 5 lightnesses, convert back to hex. No external dependency — use `colorsys` (stdlib) on Claude's side. The derived `-700`/`-800` may differ by a few units from the reference values below (rounding); the reference values win when a preset name is chosen. Steel Blue is a special case: its `primary-600` sits near L 49%, so its `-700`/`-800` are set darker than the generic L 50/42 stops to keep the hover/pressed darken visible.

### Accent-stop reference (Steel Blue, default accent)

| Name        | primary-600 | primary-50 | primary-400 | primary-700 | primary-800 | primary-900 |
| ----------- | ----------- | ---------- | ----------- | ----------- | ----------- | ----------- |
| Steel Blue  | #4682B4     | #EDF3F8    | #5A9FD4     | #396A93     | #2F5879     | #2A4F72     |

> This is the HSL ramp of Steel Blue `#4682B4`, the default palette's **light** accent; its `primary-600` sits near L 49 %, so `primary-700/800` are darkened past the generic L 50/42 stops to keep the hover/pressed darken visible (preset values win over the rule). The default palette's **dark** theme uses a separate **neutral grey** accent (`primary-400` `#B3B3B3`, `primary-600` `#9E9E9E`, `primary-700` `#808080`, `primary-800` `#6B6B6B`, `primary-900` `#404040`), not this Steel Blue ramp — see `design-system.md` / `rules/qss.md` dark stops. For any other accent (named palette or custom), Claude computes the 5 stops by the rule above (one hue, both themes) and announces them before writing.

### `onPrimary` — text on the accent

`onPrimary` is `#FFFFFF` if the accent's relative luminance keeps white text ≥ 4.5:1 (≥ 3:1 acceptable for large/UI), otherwise a near-black (`#111827`). Used in `QPushButton#btn_primary` text. Announced with the rest of the palette. When the light and dark accents differ (default palette: Steel Blue light, grey `#9E9E9E` dark), `onPrimary` is computed per theme: `#FFFFFF` in `styles_light.qss`, near-black (`#1C1C1C`) in `styles_dark.qss`.

### Named palettes & custom input

The 5 named palettes (each = 5 light roles) and the custom-palette flow live in `design-system.md §2` and are presented by `p1-scoping`. For any custom palette Claude computes **all** derived tokens (light supporting + full dark theme + accent stops + `onPrimary`) and announces the resolved values before writing them to the QSS sheets and `config.py`.

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
