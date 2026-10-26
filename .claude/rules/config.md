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

# Toast position — see `layout.md`
TOAST_POSITION: str = "top-right"

# Salesforce CLI (if enabled in Phase 1) — see @rules/sf-cli.md
SF_CLI_PATH: str = ""                          # empty = resolve "sf" from PATH (shutil.which); set = absolute path (e.g. sf.exe)
SF_CLI_TIMEOUT: int = 60                        # seconds per sf invocation

# Splash (if enabled in Phase 3) — painted programmatically, not QSS-stylable (documented exception, like ICON_COLORS). See @rules/splash.md
SPLASH_MIN_DURATION_MS: int = 1200             # minimum on-screen time before dismissal
SPLASH_COLORS: dict = {
    "light": {"bg": "#FFFFFF", "text": "#0F181E"},   # bg / text (derived light neutrals)
    "dark":  {"bg": "#111519", "text": "#F2F5F7"},   # bg / text (derived dark neutrals)
}

# Animation — design-system.md §6 (the only animated visuals: drawer slide + SlidingUnderline)
ANIM_DEFAULT_MS: int = 160                     # short functional animations (ease-out)
ANIM_SLOW_MS: int = 240                        # drawer slide, signature underline (ease-out)
ANIMATIONS_ENABLED: bool = True                # reduced motion: set at startup from animations_enabled() (utils/helpers.py); False → animations snap (design-system §6, §12)

# Accent stops — derived from the palette accent (primary-600 AFTER the AA darkening, see below). Neutrals
# (bg/text/border) live in the QSS sheets, not here. See @rules/config.md "Deriving the full palette".
PRIMARY_50:  str = "#EDF3F8"   # light selection bg
PRIMARY_400: str = "#91B6D4"   # dark foreground accent (active text/border/ring/underline/icon)
PRIMARY_600: str = "#3D729E"   # AA-darkened accent: light foreground, primary button fill (both themes)
PRIMARY_700: str = "#396A93"   # primary button hover (primary-600 minus 3 points of L)
PRIMARY_800: str = "#356388"   # primary button pressed (primary-600 minus 6 points of L)
PRIMARY_900: str = "#24425C"   # dark selection bg
ON_PRIMARY:  str = "#FFFFFF"   # text on the primary and danger fills (white, both themes; white always passes after the darkening)

# Lucide icon colors — per-theme, consumed by utils/icons.py (technical constraint: not styleable via QSS)
# Values are the DERIVED tokens (accent-tinted neutrals + per-project semantics, design-system §2/§10)
ICON_SM: int = 16
ICON_MD: int = 20
ICON_LG: int = 24
ICON_STROKE: float = 1.75      # Lucide stroke width (design-system §10)
ICON_COLORS: dict = {
    "light": {
        "default":  "#5A6670",   # text-subtle
        "active":   PRIMARY_600,
        "success":  "#328F6D",   # success-600
        "warning":  "#A58327",   # warning-600
        "danger":   "#BA3B52",   # danger-600
        "info":     PRIMARY_600, # info = accent
        "muted":    "#98A4AE",   # text-muted
        "on-primary": ON_PRIMARY,
    },
    "dark": {
        "default":  "#A3AEB8",   # text-subtle dark
        "active":   PRIMARY_400,
        "success":  "#6EC4A4",   # success-600 dark
        "warning":  "#D2B460",   # warning-600 dark
        "danger":   "#CB7282",   # danger-600 dark
        "info":     PRIMARY_400, # info = accent dark
        "muted":    "#5F6C77",   # text-muted dark
        "on-primary": ON_PRIMARY,
    }
}

# Native QPalette roles QSS cannot reach (placeholder text, tooltip base, sort arrow, disabled text of unstyled
# widgets, native popups) — applied with the sheet by utils/styles.py apply_theme (design-system.md §2). Same
# values as the sheets: window/base = bg, text = text, placeholder = text-subtle, highlight = primary-bg,
# tooltip_base = bg-elevated, disabled_text = the pre-blended disabled-text.
NATIVE_PALETTE: dict = {
    "light": {"window": "#FFFFFF", "window_text": "#0F181E", "base": "#FFFFFF", "text": "#0F181E",
              "button": "#FFFFFF", "button_text": "#0F181E", "highlight": "#EDF3F8", "highlighted_text": "#0F181E",
              "placeholder": "#5A6670", "tooltip_base": "#FFFFFF", "tooltip_text": "#0F181E",
              "link": PRIMARY_600, "disabled_text": "#9FA3A5"},
    "dark":  {"window": "#111519", "window_text": "#F2F5F7", "base": "#111519", "text": "#F2F5F7",
              "button": "#111519", "button_text": "#F2F5F7", "highlight": "#24425C", "highlighted_text": "#F2F5F7",
              "placeholder": "#A3AEB8", "tooltip_base": "#222930", "tooltip_text": "#F2F5F7",
              "link": PRIMARY_400, "disabled_text": "#6B6F72"},
}
```

Any constant reused in more than one file goes into `config.py`.

---

## Deriving the full palette

In Phase 1 the user picks a **named palette** or enters a **custom palette**: the accent is mandatory (→ `primary-600`), the four other roles are optional overrides (fond principal → `bg`, fond secondaire → `bg-subtle`, texte → `text`, détails → `border`). Claude derives everything else — the accent stops (with the **AA darkening** of `primary-600`, below), `text-on-primary`, the **accent-tinted neutrals** and surface ladder for both themes (`bg-panel` included), the **per-project semantic colors** (hue anchors harmonized ±6° toward the accent; info = accent; `danger-fill`) and the pre-blended `disabled-*` colors — and writes literal hex into `styles_light.qss` / `styles_dark.qss` and `config.py`. Role→token mapping, HSL tinting targets, override mix rules, and semantic anchors: `design-system.md §2`. Explicit overrides win over the tinted targets. After deriving, Claude runs the WCAG AA check (`design-system.md §12`, including each derived semantic pair) and reports any failure without blocking.

> The neutral and semantic tokens (`bg`, `bg-subtle`, `bg-muted`, `bg-elevated`, `bg-panel`, `text*`, `border*`, `*-50/600/700/800`, `danger-fill`, `disabled-*`, `overlay`) live **in the QSS sheets**, not in `config.py`; only the accent stops, `ICON_COLORS` (+ `ICON_STROKE`/sizes and the `ANIM_*` constants), `NATIVE_PALETTE`, and — if the splash screen is on (Phase 3) — `SPLASH_COLORS` live in `config.py`. `NATIVE_PALETTE` carries the same neutral values as the sheets for the roles QSS cannot reach; keep it in sync with them. `SPLASH_COLORS` mirrors the `bg`/`text` neutrals per theme because a `QSplashScreen` is painted programmatically and cannot be styled via QSS (`@rules/splash.md`); keep it in sync with the sheets. The derivation populates both.
>
> The default palette (Steel Blue) and every named/custom palette share **one chromatic accent ramp** across both themes: the same `PRIMARY_*` values drive light and dark, only the usage flips (`primary-600` for the button fill and light foreground; `primary-400` for the dark foreground; `primary-50`/`900` for light/dark selection). The surfaces are **accent-tinted** in both themes (HSL targets, `design-system.md §2`) and form a four-level ladder (canvas / chrome / panel / floating) — the achromatic-grey default is retired.

### Accent stops — HSL rule and AA darkening

The accent is the source color; Claude derives `primary-600` and the other 5 stops by a deterministic HSL-based rule — same hue (`H`), same saturation (`S`), only lightness (`L`) changes.

| Token         | HSL formula                                                    | Visual role                |
| ------------- | -------------------------------------------------------------- | -------------------------- |
| `primary-50`  | `H` unchanged · `S` unchanged · `L` = 95%                      | Selection bg (light)       |
| `primary-400` | `H` unchanged · `S` unchanged · `L` = 70%                      | Active text, ring, icon (dark) |
| `primary-600` | the accent, **darkened** by the AA rule below                  | Active text/border (light), primary button fill (both themes) |
| `primary-700` | `primary-600` minus 3 points of `L`                            | Primary button hover       |
| `primary-800` | `primary-600` minus 6 points of `L`                            | Primary button pressed     |
| `primary-900` | `H` unchanged · `S` unchanged · `L` = 25%                      | Selection bg (dark)        |

**AA darkening** (`design-system.md §2`): lower the accent's `L` in steps of 1 point until three pairs all reach 4.5:1: white on it, it on `bg`, and it on `primary-50`. An accent that already passes keeps its value. `text-on-primary` is then `#FFFFFF`: after the darkening, white always passes. Method: convert the accent hex to HSL, loop on `L` with the WCAG relative-luminance ratio, convert back to hex. No external dependency: use `colorsys` (stdlib) on Claude's side. Announce both the source accent and the resulting `primary-600`. The derived stops may differ by a few units from the reference values below (rounding); the reference values win when a preset name is chosen.

### Accent-stop reference (Steel Blue, default accent)

| Name              | accent  | primary-600 | primary-50 | primary-400 | primary-700 | primary-800 | primary-900 |
| ----------------- | ------- | ----------- | ---------- | ----------- | ----------- | ----------- | ----------- |
| Steel Blue (def.) | #4682B4 | #3D729E     | #EDF3F8    | #91B6D4     | #396A93     | #356388     | #24425C     |

> The other named palettes (Teal `#0D9488` -> `primary-600` `#0B7F74`, Forest `#059669` -> `#04805A`, Slate `#4F46E5` and Ruby `#BE123C` unchanged, Amber `#B45309` unchanged) are in `design-system.md §2`; their remaining stops follow the rule above. Steel Blue (default) is a single chromatic ramp used in **both** themes (preset values win over the rule). `info` **is** the accent by definition (`info-600` = `primary-600` light / `primary-400` dark, `design-system.md §2`) — no overlap to manage. For any accent (named palette or custom), Claude computes the stops by the rule above (one hue, both themes) and announces them before writing.

### `ON_PRIMARY` — text on the accent

`ON_PRIMARY` is `#FFFFFF`: after the AA darkening, white text on `primary-600` is always ≥ 4.5:1 (5.12:1 for Steel Blue). It is one value across both themes and also the text of the Danger button (`text-on-danger`). It mirrors `text-on-primary` for icons drawn on a filled button (`ICON_COLORS["on-primary"]`).

### Pre-blended disabled colors

QSS has no `opacity`: Claude writes each `disabled-*` token (`disabled-text`, `disabled-text-subtle`, `disabled-border-strong`, `disabled-primary`, `disabled-danger`, `disabled-on-primary`) as a literal, computed once per theme as the token mixed over `bg` at 0.4 (sRGB). The `overlay` scrim is `text` with alpha 0.4 (`rgba(r, g, b, 102)`). Default-palette values: `design-system.md §2`. `NATIVE_PALETTE["…"]["disabled_text"]` is the `disabled-text` value.

### Named palettes & custom input

The 6 named palettes (each defined by its **accent alone**, plus optional role overrides for Amber) and the custom-palette flow (1 mandatory accent hex + up to 4 optional overrides) live in `design-system.md §2` and are presented by `p1-scoping`. For any palette Claude computes **all** derived tokens (accent stops with the AA darkening + `ON_PRIMARY` + accent-tinted neutrals and surface ladder for both themes + per-project semantics + `disabled-*`) and announces the resolved values before writing them to the QSS sheets and `config.py`.

---

## Persisted preferences — default values

Enabled if Phase 1 preferences = Yes. Stored in `preferences.json` at the **project root** (gitignored). In `.exe` packaging mode, move to `%APPDATA%/[AppName]/preferences.json`.

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
PySide6>=6.8.0
```

Loose versions (`>=`), pinned to the minimum version validated in Phase 1. Icons need **no dependency**: Lucide SVGs are vendored into `resources/icons/` and rendered via `QtSvg`, which ships with PySide6 (`design-system.md §10`).

### Conditional dependencies

| Phase 1 condition                    | Dependency added to requirements.txt    |
| ------------------------------------ | --------------------------------------- |
| DB = SQLite                          | none (sqlite3 stdlib)                   |
| DB = PostgreSQL                      | `psycopg[binary]>=3.2.0`                |
| DB = JSON or CSV                     | none                                    |
| i18n = Yes                           | none (PySide6.QtCore.QTranslator native)  |
| Salesforce CLI = Yes                 | none (`subprocess` + `shutil` stdlib — @rules/sf-cli.md) |
| Secrets to store (validated Phase 1) | `keyring>=25.0` (@rules/security.md §3) |
| Packaging = Yes                      | `pyinstaller>=6.15.0` (requirements-dev.txt) |

> **Version maintenance**: these versions reflect the state validated at the time of writing and **age quickly** — treat every version number above as *indicative*, not authoritative. Before pinning, re-confirm each floor against PyPI (`pip index versions <pkg>`) and **verify the pinned floor is an actually released version** (a `>=X.0` floor for a not-yet-released major would make `pip install` fail). The loose-version rule and the structure stay; the numbers are refreshed per project in Phase 1.

---

## requirements-dev.txt — if tests enabled OR for pro use

```
pytest>=8.0.0,<9.0.0
pytest-qt>=4.4.0
ruff>=0.15.0
mypy>=2.0.0
```

> pytest is **capped `<9.0.0`**: pytest 9.x has shipped (9.1.x), but pytest-qt's latest is still 4.5.0, which does not yet document pytest 9 support — the cap is load-bearing, lift it once pytest-qt confirms pytest 9. mypy 2.x enables `--strict-bytes` and `--local-partial-types` by default — generated code must pass with those.

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
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]
ignore = []

[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = true
exclude = ["tests/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
qt_api = "pyside6"
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

## Windows packaging (.exe) — opt-in in Phase 1

If packaging = Yes, a final mini-batch delivers `build.spec` + a `build.ps1` script. Tool: `pyinstaller>=6.15.0` (added to `requirements-dev.txt`).

```bash
pyinstaller --onefile --windowed --name [AppName] main.py ^
            --add-data "resources;resources" ^
            --icon resources/icon.ico
```

Details:
- Resource paths handled via `helpers.resource_path()` which resolves `sys._MEIPASS` in bundled mode.
- `preferences.json` and `logs/` moved to `%APPDATA%/[AppName]/` in bundled mode.
- `build.spec` is **committed** (a source file, not matched by the anchored `/build/` output pattern — see the `## .gitignore` section).
- `.exe` signing: out of the generator's scope (done separately with `signtool`).

### Application icon

- File: `resources/icon.ico`, multi-resolution (16→256px, 256 mandatory).
- Window (taskbar): `app.setWindowIcon(QIcon(helpers.resource_path("resources/icon.ico")))` in `main.py`.
- Executable: `--icon resources/icon.ico` in `build.spec` (if packaging, Phase 1).
- If the user provides no icon in Phase 1: OS default icon, noted in the generated README.
- **Splash icon (if the splash screen is on, Phase 3)**: the splash reuses this `resources/icon.ico`. If no icon was set in Phase 1 and the user provides a splash icon path in Phase 3, save it as `resources/icon.ico` — it then serves the window/taskbar and packaging too. No icon at all → text-only splash. See `@rules/splash.md`.

## `.gitignore`

Delivered at the project root in the last batch (`@rules/mvc.md` batch table · `/python-p5-development`). Single source of truth for what stays out of the repo. Comments in English (the authoring language). Socle common to every stack + the Python build additions on top:

```gitignore
# --- Python: bytecode, build, env ------------------------------------------
__pycache__/
*.py[cod]
.venv/
venv/
/dist/
/build/
*.egg-info/
.env

# --- App runtime data (dev only; moves to %APPDATA%/[AppName]/ when packaged) -
/data/
/logs/
/preferences.json

# --- Claude Code -----------------------------------------------------------
# Personal, never committed.
.claude/settings.local.json
.claude/agent-memory/
# NOTE: .claude/settings.json IS a delivered asset — do NOT ignore it.

# Local work plan — never committed.
tasks/

# Private specs. Only the published changelog is committed.
docs/*
!docs/release/
docs/release/*
!docs/release/CHANGELOG.md

# OS noise.
.DS_Store
Thumbs.db
desktop.ini
```

- **Build outputs are anchored** (`/dist/`, `/build/`) — the leading slash confines each pattern to the repo root, so a nested `build/` or `dist/` folder deeper in the tree is not swept by accident. `build.spec` (packaging) is a file, not the `build/` directory: the trailing-slash pattern leaves it tracked.
- **App runtime data is anchored to the root** (`/data/`, `/logs/`, `/preferences.json`) — in dev the SQLite DB (`config.DB_PATH = "data/…"`), the rotating logs (`config.LOG_DIR = "logs"`), and `preferences.json` are written at the project root (`@rules/security.md §4`, `@rules/db.md`, `@rules/logging.md`); in `.exe` packaging mode they move to `%APPDATA%/[AppName]/` and are not produced at the root at all. Never commit user data (DB/prefs/logs may hold PII).
- **Never ignored** (delivered assets): `docs/release/CHANGELOG.md` (the negated pattern above), `.claude/settings.json`, the generated root `CLAUDE.md`, `tests/`, and `scripts/` (`seed.py` / `build.ps1` / the i18n scripts must ship).
- Verify the template with `git add -A` + `git status`, **not** only `git check-ignore` — the negation rules make `check-ignore` misleading.

## Integrity verification

Detailed in `@rules/verification.md`. Key points: every constant reused in more than one file lives in `config.py`; the only colors there are the accent stops, `ICON_COLORS` and — if the splash is on — `SPLASH_COLORS` (the neutrals stay in the QSS sheets, and the derived values must match them); `requirements.txt` / `requirements-dev.txt` list only Phase 1-validated dependencies, with floors re-confirmed against PyPI as actually released versions; `pyproject.toml` delivered with the ruff / mypy / pytest configuration; `build.spec` + `scripts/build.ps1` delivered and `build.spec` committed only when packaging is enabled (Phase 1).
