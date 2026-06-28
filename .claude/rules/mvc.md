# Strict MVC rules

## Separation of responsibilities

- `models/`: business logic, data access. Never PyQt6 except `QObject`/`pyqtSignal`.
- `views/`: PyQt6 widgets only. No business logic. Emit signals.
- `controllers/`: connect View signals → Model. No layout.
- Unidirectional imports: Controller → Model + View. Never Model → View.
- One entity = one file. Constants in `config.py`.

## Mandatory structure

```
models/
├── __init__.py
├── exceptions.py          # Named business exceptions (+ SfCliNotFoundError/SfCommandError if sf)
├── sf_cli.py              # sf runner + typed helpers (if Salesforce CLI) — @rules/sf-cli.md
└── [entity]_model.py      # One file per entity

views/
├── __init__.py
├── main_window.py         # Main window (topbar, global layout)
├── toast_manager.py       # Toast system
├── org_manager_view.py    # Org Manager QTreeView (if Salesforce CLI) — @rules/sf-cli.md
└── [entity]_view.py       # One file per view

controllers/
├── __init__.py
├── org_manager_controller.py  # Org Manager wiring (if Salesforce CLI) — @rules/sf-cli.md
└── [entity]_controller.py # One file per entity

utils/
└── helpers.py             # Pure functions only — zero PyQt6, zero business logic

tests/                     # If tests enabled in Phase 1 — see @rules/tests.md
├── __init__.py
├── conftest.py
├── test_helpers.py
├── models/
├── controllers/
└── views/
```

## utils/helpers.py — allowed content only

- Date, number, string formatting.
- Data validation (email, numeric…).
- JSON file read/write (preferences).
- Generic conversion functions.

## Batch delivery

### Without tests (Phase 1 Q5 = No)

**Small project (3 batches):**

| Batch | Content                                                                          |
| ----- | -------------------------------------------------------------------------------- |
| 1     | `config.py` + `models/` (including `db.py` and `migrations.py` if DB)             |
| 2     | `views/` + `controllers/`                                                         |
| 3     | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |

**Medium / Large project (4 batches):**

| Batch | Content                                                                          |
| ----- | -------------------------------------------------------------------------------- |
| 1     | `config.py` + `models/` (including `db.py` and `migrations.py` if DB)             |
| 2     | `views/`                                                                          |
| 3     | `controllers/`                                                                   |
| 4     | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |

### With tests (Phase 1 Q5 = Yes)

**Small project (4 batches):**

| Batch | Content                                                                          |
| ----- | -------------------------------------------------------------------------------- |
| 1     | `config.py` + `models/`                                                          |
| 2     | `views/` + `controllers/`                                                         |
| 3     | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |
| 4     | `tests/` + `requirements-dev.txt` + pytest instructions                          |

**Medium / Large project (5 batches):**

| Batch | Content                                                                          |
| ----- | -------------------------------------------------------------------------------- |
| 1     | `config.py` + `models/`                                                          |
| 2     | `views/`                                                                          |
| 3     | `controllers/`                                                                   |
| 4     | `main.py` + `utils/` + `resources/styles_*.qss` + `requirements.txt` + `pyproject.toml` + instructions |
| 5     | `tests/` + `requirements-dev.txt` + pytest instructions                          |

> **Salesforce CLI integration (if Phase 1 = Yes)** — no dedicated batch. `sf_cli.py` (runner + helpers) ships in **Batch 1** with `config.py` + `models/`; `org_manager_view.py` ships with the views batch; `org_manager_controller.py` ships with the controllers batch. It counts toward the size (`## CALIBRATION` in `CLAUDE.md`). See `@rules/sf-cli.md`.

### Content of the `utils/` folder

- `utils/helpers.py` — pure functions (formatting, validation, JSON)
- `utils/logger.py` — logging configuration (see `@rules/logging.md`)
- `utils/resource_path.py` — PyInstaller `sys._MEIPASS` helper (if packaging opt-in)

### Format

Announcement format: `Batch N/[total] — [content]`
Each file delivered as a complete, self-contained block.
**Automatic chaining** between batches — no confirmation requested.
The user can interrupt at any time.
If the user reports an anomaly after a batch: free invocation of any correction command.

## Integrity verification

Per-batch and cross-file integrity checks (Python syntax, used/unidirectional imports, MVC responsibilities, signals/slots, zero hardcoded visual value, source↔test mapping) live in **`rules/verification.md`** — the single source of truth for verification. Run them silently every batch; report only on a discrepancy. Cross-file checks run on the last batch.

## Anti-patterns — what NOT to do (MVC)

- **Do not** import a View from a Model, or call `show_toast` / touch a widget from a Model. Models are PyQt6-free except `QObject`/`pyqtSignal`.
- **Do not** put business logic or data access in a View or a Controller. Views render and emit signals; controllers wire and intercept; logic lives in models.
- **Do not** propagate a business exception out of the controller — intercept it and call `view.show_toast(...)` (see `@rules/errors.md`).
- **Do not** put PyQt6, business logic, or data access in `utils/helpers.py` — pure functions only.
- **Do not** spread one entity across more files than `model + view + controller`. If it grows, that is a contract change → declare the deviation (Phase 4 protocol).
- **Do not** hardcode a shared constant in one layer — promote it to `config.py`.

## Anomaly resolution — cleanup protocol

As soon as the definitive solution is identified and delivered:

```
Anomaly resolved. Elements to remove from the previous attempts:

File [name]:
- [line / block / import / objectName to delete]
```

Cover all affected files. Then offer: "Do you want to remember this point? `/python-save-memory`"

## Post-delivery adjustments

Isolated fix on the affected file + its direct dependencies. Deliver the complete fixed file (full rewrite via `Write`, never a partial diff).
