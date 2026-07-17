# Python App Generator - Unified

> Claude Code generator for **Windows desktop apps** - Python · PySide6 · QSS · MVC.

Part of a family of Claude Code generators. See also [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator), [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator), [sf-node-generator](https://github.com/TiercelinQ/sf-node-generator), and [vscode-ext-generator](https://github.com/TiercelinQ/vscode-ext-generator).

Unified edition: the full generation pipeline **plus** post-delivery maintenance skills, an explicit role per skill, persisted specs, centralized executable verification, and native memory.

---

## What it does

A structured prompt system that generates complete, production-ready PySide6 desktop applications through a 5-phase cycle, then maintains them:

1. **Scoping** - 8 questions (objective, DB, prefs, i18n, tests, icon, packaging, Salesforce CLI opt-in) + color palette (named or custom; accent + optional overrides, neutrals and semantics derived, WCAG AA check)
2. **Featuring** - structured feature sheet, explicit out-of-scope, locked sizing
3. **Surfaces** - topbar tabs, drawer/modal, toast position (6 positions), splash screen
4. **Architect** - full file tree, QSS token table, source→test mapping - locked before any code is written
5. **Development** - auto-chained batch delivery, seed script if a DB is used, dedicated test batch if opted-in

Each phase writes a spec in the user's language to `docs/specs/` (`01-scoping` … `04-architect`); the contract is the source of truth.

**Maintenance commands**: `/python-add-feature` (incremental work via a contract diff), `/python-trace-feature` (trace behavior), `/python-fix-issue` (root-cause debugging with a decision tree), `/python-refactor-code` (validated, behavior-preserving), `/python-migrate-design` (convert a v1.x app to design system v2.0), `/python-release` (cut a SemVer release from the accumulated changelog), `/python-run-tests` (executable verification). Plus `/python-load-project` and `/python-generate-readme` to load/document existing apps.

Every generated app enforces the same visual design system and strict MVC architecture.

---

## Generated app stack

| Element        | Value                                                       |
| -------------- | ----------------------------------------------------------- |
| Language       | Python 3.12+                                                |
| Framework      | PySide6                                                       |
| Architecture   | MVC strict                                                  |
| Styling        | Centralized QSS - `styles_light.qss` + `styles_dark.qss`    |
| Icons          | Lucide (vendored SVGs + `utils/icons.py`)                   |
| i18n           | PySide6.QtCore.QTranslator FR/EN (opt-in)                     |
| Tests          | pytest + pytest-qt (opt-in)                                 |
| Logging        | stdlib `logging` + RotatingFileHandler                      |
| DB             | sqlite3 / psycopg / json / csv - versioned migrations       |
| Salesforce CLI | `sf` v2 wrapper via subprocess + starter Org Manager (opt-in) |
| Packaging      | PyInstaller (opt-in)                                        |
| Tooling        | ruff + mypy via `pyproject.toml`                            |
| Quality        | PEP 8 · type hints · docstrings · `sys.excepthook` + toast  |

---

## Requirements

```bash
claude --version    # Claude Code CLI - installed and authenticated
python --version    # Python 3.12+
```

---

## Getting started

```bash
git clone https://github.com/TiercelinQ/python-app-generator.git
cd python-app-generator
claude
```

Then in Claude Code:

```
/python-app
```

---

## Commands

| Command                 | Action                                             |
| ----------------------- | -------------------------------------------------- |
| `/python-app`           | Start menu (4 entry points incl. maintenance)      |
| `/python-p1-scoping`       | Scoping - 8 questions + color palette              |
| `/python-p2-featuring`       | Featuring - requirements sheet + locked sizing     |
| `/python-p3-surfaces`        | Surfaces - layout proposal + customization        |
| `/python-p4-architect`       | Architect - locked architecture contract           |
| `/python-p5-development` | Auto-chained batch delivery                        |
| `/python-add-feature`          | Add a feature to a shipped project (diff first)    |
| `/python-trace-feature`              | Trace a feature across the MVC layers              |
| `/python-fix-issue`                  | Fix a bug - decision tree, root cause              |
| `/python-refactor-code`             | Refactor under explicit validation only            |
| `/python-migrate-design`            | Convert a v1.x app to design system v2.0           |
| `/python-release`                   | Cut a SemVer release from the accumulated changelog|
| `/python-run-tests`                 | Executable verification (ruff, mypy, pytest)       |
| `/python-load-project`       | Load an existing project from its specs/README     |
| `/python-generate-readme`      | Generate README.md for an existing project         |
| `/python-save-session`              | Save current session state                         |
| `/python-show-state`               | Current project status                             |
| `/python-show-contract`              | Display locked architecture contract               |
| `/python-save-memory`            | Persist a note in Claude Code native memory        |

---

## Generated app structure

```
my_app/
├── main.py                        # Entry point - logger, migrations, excepthook
├── config.py                      # Constants · PRIMARY_* · ICON_COLORS · LOG_*
├── requirements.txt · pyproject.toml
├── README.md
├── CLAUDE.md                      # Project identity (origin, business context, deviations)
├── .claude/settings.json          # Guardrails + verification hook (self-enforced app)
├── docs/specs/                    # Generation specs (user's language): 01-scoping … 04-architect
├── docs/release/CHANGELOG.md      # SemVer changelog (Keep a Changelog, English)
├── models/
│   ├── exceptions.py              # Named business exceptions
│   ├── db.py                      # Single DB access point (if DB ≠ none)
│   ├── migrations.py              # Versioned schema migrations (if DB ≠ none)
│   └── [entity]_model.py
├── views/
│   ├── main_window.py             # Main window · topbar · install_excepthook
│   ├── toast_manager.py           # Toasts (6 positions, animation, durations)
│   └── [entity]_view.py
├── controllers/
│   └── [entity]_controller.py
├── utils/
│   ├── helpers.py                 # Pure functions (formatting, validation)
│   └── logger.py                  # Centralized logging setup
└── resources/
    ├── styles_light.qss           # Light theme - all design-system.md tokens
    ├── styles_dark.qss            # Dark theme - all design-system.md tokens
    └── i18n/                      # If i18n enabled - app_{fr,en}.{ts,qm}

# Generated only if a database is selected in Phase 1:
scripts/seed.py                    # Idempotent demo-data seed (run manually)

# Generated only if tests opted-in during Phase 1:
tests/                             # Mirrors the source structure
requirements-dev.txt               # pytest, pytest-qt
```

---

## Versioning & changelog

Every generated app carries a SemVer version and a changelog at `docs/release/CHANGELOG.md` (Keep a Changelog format, written in English). Maintenance skills (`add-feature`, `fix-issue`, `refactor-code`, `migrate-design`) accumulate entries under `## [Unreleased]`; `/python-release` freezes them into a dated version block and bumps the version source (`config.py` `APP_VERSION`, single source, no mirror). The version is never bumped silently. See `rules/versioning.md`.

---

## Design system

All generated apps share the same visual system, defined in `.claude/design-system.md` (v2.0):

- **Depth by stroke** - borders express hierarchy and elevation, zero shadows, zero gradients; soft 5px radius
- **QSS sheets** - all colors, sizes and durations are tokens; full light/dark theme via complete QSS replacement
- **System font** typography (QApplication native face, no pinned family)
- **Color palette** - one mandatory accent (+ up to 4 optional role overrides); accent-tinted neutrals, accent stops, and per-project semantic colors all derived from it (info = accent). Default "Steel Blue" + Teal, Forest, Slate, Amber, Ruby named palettes + custom palette
- **Lucide icons** (vendored SVGs, stroke 1.75) and one signature gesture: the sliding underline on tabs (`QPropertyAnimation`)
- **Toasts only** - no inline banners, no `QMessageBox` for business errors

---

## Documentation

- [GUIDE.md](GUIDE.md) - full usage guide (FR)
- `.claude/design-system.md` (v2.0) - visual token reference + changelog
- `.claude/layout.md` (v4.1) - layout companion (pattern catalog + proposed default composition) + 6 toast positions
- `.claude/rules/` - domain rules:
  - `mvc.md` · `qss.md` · `errors.md` · `config.md` · `security.md`
  - `tests.md` · `logging.md` · `i18n.md` · `db.md` · `sf-cli.md` (opt-in) · `splash.md` (opt-in)
  - `verification.md` - single source of truth for executable + static checks
  - `readme.md` - README synchronization rule
- `.claude/sf-cli-reference/` - `sf` v2 command/flag catalog (loaded by section when the Salesforce integration is on)

---

## Generator family

| Generator | Stack | Target |
| --------- | ----- | ------ |
| [python-app-generator](https://github.com/TiercelinQ/python-app-generator) | Python · PySide6 · QSS | Windows desktop |
| [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator) | Node.js · Electron · React · TS | Windows desktop |
| [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator) | Flutter · Dart · Riverpod | Android |
| [sf-node-generator](https://github.com/TiercelinQ/sf-node-generator) | Node.js · TypeScript · Salesforce CLI | Headless CLI |
| [vscode-ext-generator](https://github.com/TiercelinQ/vscode-ext-generator) | TypeScript · esbuild · native theming | VS Code extension |

---

## License

MIT
