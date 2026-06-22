# Python App Generator - Unified

> Claude Code generator for **Windows desktop apps** - Python · PyQt6 · QSS · MVC.

Part of a family of Claude Code generators. See also [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator), [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator) and [next-app-generator](https://github.com/TiercelinQ/next-app-generator).

Unified edition: the full generation pipeline **plus** post-delivery maintenance skills, an explicit role per skill, persisted specs, centralized executable verification, and native memory.

---

## What it does

A structured prompt system that generates complete, production-ready PyQt6 desktop applications through a 5-phase cycle, then maintains them:

1. **Scoping** - 6 questions (objective, DB, prefs, i18n, tests, packaging) + color palette (named or custom; 5 roles, dark + supporting tokens derived, WCAG AA check)
2. **Featuring** - structured feature sheet, explicit out-of-scope, locked sizing
3. **Designing** - navigation, drawer/modal, toast position (6 positions)
4. **Architect** - full file tree, QSS token table, source→test mapping - locked before any code is written
5. **Development** - auto-chained batch delivery, seed script if a DB is used, dedicated test batch if opted-in

Each phase writes a spec in the user's language to `docs/specs/` (`01-scoping` … `04-architect`); the contract is the source of truth.

**Maintenance commands**: `/python-add-feature` (incremental work via a contract diff), `/python-trace-feature` (trace behavior), `/python-fix-issue` (root-cause debugging with a decision tree), `/python-refactor-code` (validated, behavior-preserving), `/python-run-tests` (executable verification). Plus `/python-load-project` and `/python-generate-readme` to load/document existing apps.

Every generated app enforces the same visual design system and strict MVC architecture.

---

## Generated app stack

| Element        | Value                                                       |
| -------------- | ----------------------------------------------------------- |
| Language       | Python 3.10+                                                |
| Framework      | PyQt6                                                       |
| Architecture   | MVC strict                                                  |
| Styling        | Centralized QSS - `styles_light.qss` + `styles_dark.qss`    |
| Icons          | qtawesome (Font Awesome)                                    |
| i18n           | PyQt6.QtCore.QTranslator FR/EN (opt-in)                     |
| Tests          | pytest + pytest-qt (opt-in)                                 |
| Logging        | stdlib `logging` + RotatingFileHandler                      |
| DB             | sqlite3 / psycopg / json / csv - versioned migrations       |
| Packaging      | PyInstaller (opt-in)                                        |
| Tooling        | ruff + mypy via `pyproject.toml`                            |
| Quality        | PEP 8 · type hints · docstrings · `sys.excepthook` + toast  |

---

## Requirements

```bash
claude --version    # Claude Code CLI - installed and authenticated
python --version    # Python 3.10+
```

---

## Getting started

```bash
git clone https://github.com/TiercelinQ/claude-python-app-generator.git
cd claude-python-app-generator
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
| `/python-p1-scoping`       | Scoping - 6 questions + color palette              |
| `/python-p2-featuring`       | Featuring - requirements sheet + locked sizing     |
| `/python-p3-designing`        | Designing - layout proposal + customization        |
| `/python-p4-architect`       | Architect - locked architecture contract           |
| `/python-p5-development` | Auto-chained batch delivery                        |
| `/python-add-feature`          | Add a feature to a shipped project (diff first)    |
| `/python-trace-feature`              | Trace a feature across the MVC layers              |
| `/python-fix-issue`                  | Fix a bug - decision tree, root cause              |
| `/python-refactor-code`             | Refactor under explicit validation only            |
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

## Design system

All generated apps share the same visual system, defined in `.claude/design-system.md`:

- **Flat design** - zero border-radius, zero shadows, zero gradients
- **QSS sheets** - all colors, sizes and durations are tokens; full light/dark theme via complete QSS replacement
- **Segoe UI** typography (Windows native)
- **Color palette** - 5 roles (main background, secondary background, accent, text, details) chosen for the light theme; dark theme and all supporting tokens derived. Default "Teal" + Steel Blue, Forest, Slate, Amber, Ruby named palettes + custom palette; semantic colors stay fixed
- **Toasts only** - no inline banners, no `QMessageBox` for business errors

---

## Documentation

- [GUIDE.md](GUIDE.md) - full usage guide (FR)
- `.claude/design-system.md` (v1.4) - visual token reference + changelog
- `.claude/layout.md` (v2.2) - layout reference + 6 toast positions
- `.claude/rules/` - domain rules:
  - `mvc.md` · `qss.md` · `errors.md` · `config.md` · `security.md`
  - `tests.md` · `logging.md` · `i18n.md` · `db.md`
  - `verification.md` - single source of truth for executable + static checks

---

## Generator family

| Generator | Stack | Target |
| --------- | ----- | ------ |
| [claude-python-app-generator](https://github.com/TiercelinQ/claude-python-app-generator) | Python · PyQt6 · QSS | Windows desktop |
| [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator) | Node.js · Electron · React · TS | Windows desktop |
| [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator) | Flutter · Dart · Riverpod | Android |
| [next-app-generator](https://github.com/TiercelinQ/next-app-generator) | Next.js · React · TS · Postgres | Web (self-hosted) |

---

## License

MIT
