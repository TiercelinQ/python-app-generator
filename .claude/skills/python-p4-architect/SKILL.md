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

At start: read `design-system.md`, `layout.md` (no longer auto-imported), `rules/mvc.md` (tree, batches) and `rules/qss.md` (tokens → QSS). **If the Salesforce CLI integration is on (Phase 1), also read @rules/sf-cli.md** (runner, exceptions, Org Manager scaffold). Read `docs/specs/01-scoping.md` through `03-designing.md` for the validated decisions.

Present the complete project tree with the role of each file, then the QSS token table. Output format (in the user's language):

```
## Architectural contract — [NOM_APP]

### File tree

[nom_app]/
├── main.py                        # Entry point — QApplication, MainWindow, logger, migrations, excepthook
├── config.py                      # Global constants, ICON_COLORS, PRIMARY_* (+ SPLASH_* if splash)
├── requirements.txt
├── pyproject.toml                 # ruff, mypy, pytest config
├── docs/specs/                    # Generation specs (user's language): 01-scoping … 04-architect
├── preferences.json               # Project root — generated on first launch (if Q3=Yes)
├── logs/                          # Created automatically by utils/logger.py
├── models/
│   ├── __init__.py
│   ├── exceptions.py              # Named business exceptions (+ SfCliNotFoundError/SfCommandError if sf)
│   ├── db.py                      # Single DB access point (if DB ≠ none)
│   ├── migrations.py              # Versioned migrations (if DB ≠ none)
│   ├── sf_cli.py                  # sf runner + typed helpers (if Salesforce CLI) — @rules/sf-cli.md
│   └── [entite]_model.py          # [role]
├── views/
│   ├── __init__.py
│   ├── main_window.py             # Main window, topbar, global layout, install_excepthook
│   ├── toast_manager.py           # Toasts (position, animation, queue)
│   ├── splash_screen.py           # QSplashScreen factory (if splash enabled) — @rules/splash.md
│   ├── org_manager_view.py        # Org Manager QTreeView (if Salesforce CLI) — @rules/sf-cli.md
│   └── [entite]_view.py           # [role]
├── controllers/
│   ├── __init__.py
│   ├── org_manager_controller.py  # Org Manager wiring + auth orchestration (if Salesforce CLI) — @rules/sf-cli.md
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
| bg                      | #FFFFFF      | #1C1C1C       | QMainWindow, #main_content, #topbar |
| primary-600             | #4682B4      | #4682B4       | QTabBar::tab:selected, #btn_primary |
| …                       | …            | …             | …               |

### Source → test mapping (if tests enabled)

| Source module                        | Test file                                     |
| ------------------------------------ | --------------------------------------------- |
| `models/[entite]_model.py`           | `tests/models/test_[entite]_model.py`         |
| `models/sf_cli.py` (if sf)           | `tests/models/test_sf_cli.py` (subprocess mocked) |
| `controllers/[entite]_controller.py` | `tests/controllers/test_[entite]_controller.py` |
| `controllers/org_manager_controller.py` (if sf) | `tests/controllers/test_org_manager_controller.py` |
| `views/[entite]_view.py`             | `tests/views/test_[entite]_view.py` (smoke)   |
| `utils/helpers.py`                   | `tests/test_helpers.py`                       |
```

If the Salesforce CLI integration is on, include the `sf:org:*`-equivalent surface in the contract: the `models/sf_cli.py` runner/helpers, the Org Manager view/controller, and the documented `sf` runtime prerequisite (`SF_CLI_PATH`). See @rules/sf-cli.md.

If the splash screen is on (Phase 3), include it in the contract: `views/splash_screen.py`, the `SPLASH_MIN_DURATION_MS` + `SPLASH_COLORS` constants in `config.py`, the `main.py` orchestration (`create_splash` before `MainWindow`, `splash.finish(window)` after the min duration), and the icon source (provided path, packaging icon reused, or text-only). See @rules/splash.md.

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
