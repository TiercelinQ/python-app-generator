# Python App Generator — unified

> Claude Code generator for **Windows desktop apps** — Python · PyQt6 · QSS · MVC.

Part of a family of Claude Code generators. See also [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator) and [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator).

Unified edition: the full generation pipeline **plus** post-delivery maintenance skills, an explicit role per skill, persisted specs, centralized executable verification, and native memory.

---

## What it does

A structured prompt system that generates complete, production-ready PyQt6 desktop applications through a 5-phase cycle, then maintains them:

1. **Scoping** — 6 questions (objective, DB, prefs, i18n, tests, packaging) + primary color (HSL derivation from a single hex)
2. **Requirements** — structured feature sheet, explicit out-of-scope, locked sizing
3. **Layout** — navigation, drawer/modal, toast position (6 positions)
4. **Architecture contract** — full file tree, QSS token table, source→test mapping — locked before any code is written
5. **Development** — auto-chained batch delivery, dedicated test batch if opted-in

Each phase writes a French spec to `docs/specs/` (`01-cadrage` … `04-contrat`); the contract is the source of truth.

**Maintenance commands**: `/feature-add` (incremental work via a contract diff), `/analyze` (trace behavior), `/fix` (root-cause debugging with a decision tree), `/refactor` (validated, behavior-preserving), `/test` (executable verification). Plus `/charger-projet` and `/generate-readme` to load/document existing apps.

Every generated app enforces the same visual design system and strict MVC architecture.

---

## Generated app stack

| Element        | Value                                                       |
| -------------- | ----------------------------------------------------------- |
| Language       | Python 3.10+                                                |
| Framework      | PyQt6                                                       |
| Architecture   | MVC strict                                                  |
| Styling        | Centralized QSS — `styles_light.qss` + `styles_dark.qss`    |
| Icons          | qtawesome (Font Awesome)                                    |
| i18n           | PyQt6.QtCore.QTranslator FR/EN (opt-in)                     |
| Tests          | pytest + pytest-qt (opt-in)                                 |
| Logging        | stdlib `logging` + RotatingFileHandler                      |
| DB             | sqlite3 / psycopg / json / csv — versioned migrations       |
| Packaging      | PyInstaller (opt-in)                                        |
| Tooling        | ruff + mypy via `pyproject.toml`                            |
| Quality        | PEP 8 · type hints · docstrings · `sys.excepthook` + toast  |

---

## Requirements

```bash
claude --version    # Claude Code CLI — installed and authenticated
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
| `/phase1-cadrage`       | Scoping — 6 questions + primary color (HSL derive) |
| `/phase2-analyse`       | Requirements sheet + locked sizing                 |
| `/phase3-layout`        | Layout proposal + customization                    |
| `/phase4-contrat`       | Locked architecture contract                       |
| `/phase5-developpement` | Auto-chained batch delivery                        |
| `/feature-add`          | Add a feature to a shipped project (diff first)    |
| `/analyze`              | Trace a feature across the MVC layers              |
| `/fix`                  | Fix a bug — decision tree, root cause              |
| `/refactor`             | Refactor under explicit validation only            |
| `/test`                 | Executable verification (ruff, mypy, pytest)       |
| `/charger-projet`       | Load an existing project from its specs/README     |
| `/generate-readme`      | Generate README.md for an existing project         |
| `/session`              | Save current session state                         |
| `/statut`               | Current project status                             |
| `/contrat`              | Display locked architecture contract               |
| `/memoriser`            | Persist a note in Claude Code native memory        |

---

## Generated app structure

```
my_app/
├── main.py                        # Entry point — logger, migrations, excepthook
├── config.py                      # Constants · PRIMARY_* · ICON_COLORS · LOG_*
├── requirements.txt · pyproject.toml
├── README.md
├── CLAUDE.md                      # Project identity (origin, business context, deviations)
├── .claude/settings.json          # Guardrails + verification hook (self-enforced app)
├── docs/specs/                    # Generation specs (FR): 01-cadrage … 04-contrat
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
    ├── styles_light.qss           # Light theme — all design-system.md tokens
    ├── styles_dark.qss            # Dark theme — all design-system.md tokens
    └── i18n/                      # If i18n enabled — app_{fr,en}.{ts,qm}

# Generated only if tests opted-in during Phase 1:
tests/                             # Mirrors the source structure
requirements-dev.txt               # pytest, pytest-qt
```

---

## Design system

All generated apps share the same visual system, defined in `design-system.md`:

- **Flat design** — zero border-radius, zero shadows, zero gradients
- **QSS sheets** — all colors, sizes and durations are tokens; full light/dark theme via complete QSS replacement
- **Segoe UI** typography (Windows native)
- **Slate Blue** primary color by default — change a single `primary-600` hex, the other 3 are HSL-derived
- **Toasts only** — no inline banners, no `QMessageBox` for business errors

---

## Documentation

- [GUIDE.md](GUIDE.md) — full usage guide (FR)
- `design-system.md` (v1.1) — visual token reference + changelog
- `layout.md` (v2.1) — layout reference + 6 toast positions
- `rules/` — domain rules:
  - `mvc.md` · `qss.md` · `errors.md` · `config.md` · `security.md`
  - `tests.md` · `logging.md` · `i18n.md` · `db.md`
  - `verification.md` — single source of truth for executable + static checks

---

## Generator family

| Generator | Stack | Target |
| --------- | ----- | ------ |
| [claude-python-app-generator](https://github.com/TiercelinQ/claude-python-app-generator) | Python · PyQt6 · QSS | Windows desktop |
| [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator) | Node.js · Electron · React · TS | Windows desktop |
| [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator) | Flutter · Dart · Riverpod | Android |

---

## License

MIT
