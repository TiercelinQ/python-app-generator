---
name: python-p4-architect
description: Phase 4 of the development cycle — architectural contract (full tree, role of each file, tokens → QSS table, source→test mapping), written to the contract spec and locked after validation.
model: sonnet
---

# /python-p4-architect — Architectural contract

## Role
Software architect — design the locked structure the whole build will follow.

## Goal
Produce a complete, unambiguous architectural contract that freezes the file tree, QSS mapping, and (if tests) the source→test mapping.

## Deliverable
`docs/specs/04-architect.md` (written in the user's language) — the locked source of truth + on-screen contract.

---

**Phase banner (show first)** — before anything else, output the phase banner as plain Markdown in the user's language, **never inside a code block or fenced block**. Three blocks, each on its own line: (1) H2 heading: Phase 4/5 — Architecture; (2) progress line: Scoping ✓ · Features ✓ · Design ✓ · ▶ Architecture · Development; (3) intent in italics: Lock the file/structure contract. See `## PIPELINE` in `CLAUDE.md`.

At start: read `design-system.md`, `layout.md` (no longer auto-imported), `rules/mvc.md` (tree, batches) and `rules/qss.md` (tokens → QSS). Read `docs/specs/01-scoping.md` through `03-designing.md` for the validated decisions.

Present the complete project tree with the role of each file, then the QSS token table. Output format (in the user's language):

```
## Architectural contract — [NOM_APP]

### File tree

[nom_app]/
├── main.py                        # Entry point — QApplication, MainWindow, logger, migrations, excepthook
├── config.py                      # Global constants, ICON_COLORS, PRIMARY_*
├── requirements.txt
├── pyproject.toml                 # ruff, mypy, pytest config
├── docs/specs/                    # Generation specs (user's language): 01-scoping … 04-architect
├── preferences.json               # Project root — generated on first launch (if Q3=Yes)
├── logs/                          # Created automatically by utils/logger.py
├── models/
│   ├── __init__.py
│   ├── exceptions.py              # Named business exceptions
│   ├── db.py                      # Single DB access point (if DB ≠ none)
│   ├── migrations.py              # Versioned migrations (if DB ≠ none)
│   └── [entite]_model.py          # [role]
├── views/
│   ├── __init__.py
│   ├── main_window.py             # Main window, topbar, global layout, install_excepthook
│   ├── toast_manager.py           # Toasts (position, animation, queue)
│   └── [entite]_view.py           # [role]
├── controllers/
│   ├── __init__.py
│   └── [entite]_controller.py     # [role]
├── utils/
│   ├── helpers.py                 # Pure functions (formatting, JSON, validation)
│   └── logger.py                  # Configuration logging (@rules/logging.md)
└── resources/
    ├── styles_light.qss           # Light theme — all design-system.md tokens
    ├── styles_dark.qss            # Dark theme — all design-system.md tokens
    └── i18n/                      # If i18n enabled (@rules/i18n.md): app_{fr,en}.{ts,qm}

# If tests enabled in Phase 1:
tests/                             # Miroir de la structure source (@rules/tests.md)
requirements-dev.txt               # pytest>=8.0.0, pytest-qt>=4.4.0

### Tokens → QSS rules table

| design-system.md token | Light value | Dark value | Target QSS rule |
| ----------------------- | ------------ | ------------- | --------------- |
| bg                      | #FFFFFF      | #1A1A1F       | QMainWindow, #main_content, #topbar |
| primary-600             | #4682B4      | —             | QTabBar::tab:selected, #btn_primary |
| …                       | …            | …             | …               |

### Source → test mapping (if tests enabled)

| Source module                        | Test file                                     |
| ------------------------------------ | --------------------------------------------- |
| `models/[entite]_model.py`           | `tests/models/test_[entite]_model.py`         |
| `controllers/[entite]_controller.py` | `tests/controllers/test_[entite]_controller.py` |
| `views/[entite]_view.py`             | `tests/views/test_[entite]_view.py` (smoke)   |
| `utils/helpers.py`                   | `tests/test_helpers.py`                       |
```

End with:

→ This contract is locked after validation.
  Any later deviation (merge, split, rename, addition, removal) requires:
  1. Stop.
  2. Declare the deviation + justification.
  3. Validation before resuming.

  Confirm to start Phase 5.

**Blocking rule**: do not deliver Batch 1 until validation is explicit.

## Write the spec

Once validated, write the full contract to `docs/specs/04-architect.md` (in the user's language). This file is the **locked source of truth** re-read by `/python-p5-development`, `/python-load-project`, `/python-show-contract`, `/python-add-feature`, and `/python-refactor-code`.

Chain to `/python-p5-development` after validation.
