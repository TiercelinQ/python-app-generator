# Python App Generator

> Claude Code generator for **Windows desktop apps** — Python · PyQt6 · QSS · MVC.

Part of a family of Claude Code generators. See also [electron-app-generator](https://github.com/TiercelinQ/electron-app-generator) and [flutter-app-generator](https://github.com/TiercelinQ/flutter-app-generator).

---

## What it does

A structured prompt system that generates complete, production-ready PyQt6 desktop applications through a 5-phase cycle:

1. **Scoping** — stack decisions, primary color, library validation, lot sizing
2. **Requirements** — structured feature sheet, explicit out-of-scope
3. **Layout** — navigation, drawer/modal, toast position
4. **Architecture contract** — full file tree, QSS token table — locked before any code is written
5. **Development** — files written directly to disk in batches, no manual steps

Every generated app enforces the same visual design system and strict MVC architecture.

---

## Generated app stack

| Element        | Value                                    |
| -------------- | ---------------------------------------- |
| Language       | Python 3.10+                             |
| Framework      | PyQt6                                    |
| Architecture   | MVC strict                               |
| Styling        | Centralized QSS — light/dark full sheets |
| Icons          | qtawesome (Font Awesome)                 |
| i18n           | PyQt6.QtCore.QTranslator FR/EN           |
| Quality        | PEP 8 · type hints · docstrings          |

---

## Requirements

```bash
# Claude Code CLI — installed and authenticated
claude --version

# Python 3.10+
python --version
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
| `/python-app`           | Start menu / resume session                        |
| `/phase1-cadrage`       | Scoping — questions + primary color                |
| `/phase2-analyse`       | Structured requirements sheet                      |
| `/phase3-layout`        | Layout proposal + customization                    |
| `/phase4-contrat`       | Locked architecture contract                       |
| `/phase5-developpement` | Batch delivery — files written to disk             |
| `/charger-projet`       | Load an existing project from its README.md        |
| `/generate-readme`      | Generate README.md for an existing project         |
| `/session`              | Save current session state                         |
| `/statut`               | Current project status                             |
| `/contrat`              | Display locked architecture contract               |
| `/memoriser`            | Memorize an error, decision, or preference         |

---

## Generated app structure

```
my_app/
├── main.py                        # Entry point
├── config.py                      # Constants · PRIMARY_* · ICON_COLORS
├── requirements.txt
├── README.md
├── models/
│   ├── __init__.py
│   ├── exceptions.py              # Named business exceptions
│   └── [entity]_model.py
├── views/
│   ├── __init__.py
│   ├── main_window.py             # Main window · topbar · global layout
│   ├── toast_manager.py           # Toasts (position, animation, durations)
│   └── [entity]_view.py
├── controllers/
│   ├── __init__.py
│   └── [entity]_controller.py
├── utils/
│   └── helpers.py                 # Pure functions (formatting, validation)
└── resources/
    ├── styles_light.qss           # Light theme — all design-system.md tokens
    └── styles_dark.qss            # Dark theme — all design-system.md tokens
```

---

## Design system

All generated apps share the same visual system, defined in `.claude/design-system.md`:

- **Flat design** — zero border-radius, zero shadows, zero gradients
- **QSS sheets** — all colors, sizes and durations are tokens; full light/dark theme via complete QSS replacement
- **Segoe UI** typography (Windows native)
- **Slate Blue** primary color by default — 4 token values to change the entire app color
- **Toasts only** — no inline banners, no `QMessageBox` for business errors

---

## Documentation

- [GUIDE.md](GUIDE.md) — full usage guide
- `.claude/design-system.md` — visual token reference
- `.claude/layout.md` — layout reference (topbar, toasts, drawer, modal, table, pagination)
- `.claude/rules/` — domain rules (MVC, QSS, errors, config)

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
