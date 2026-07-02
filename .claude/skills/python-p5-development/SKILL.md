---
name: python-p5-development
description: Phase 5 of the Python app generation cycle — development and batch delivery, files written directly to disk, executable verification, final README. Invoke after the architectural contract (Phase 4) is validated, and for each subsequent batch.
model: sonnet
---

# /python-p5-development — Batch development

## Role
Senior PyQt6 developer — build the contracted app to a clean, runnable state.

## Goal
Deliver the application in batches, each one ruff/mypy-clean and contract-compliant, ending with install instructions and a README.

## Deliverable
The full project source on disk + `README.md` + verified build.

---

**Phase banner (show first)** — before anything else, output the phase banner as plain Markdown in the user's language, **never inside a code block or fenced block**. Three blocks, each on its own line: (1) H2 heading: Phase 5/5 — Development; (2) progress line: Scoping ✓ · Features ✓ · Design ✓ · Architecture ✓ · ▶ Development; (3) intent in italics: Deliver the app in batches. See `## PIPELINE` in `CLAUDE.md`.

## Code rules

Apply fully: `@rules/mvc.md` · `@rules/qss.md` · `@rules/errors.md` · `@rules/config.md` · `@rules/security.md` · `@rules/tests.md` · `@rules/logging.md` · `@rules/i18n.md` · `@rules/db.md` · `@rules/sf-cli.md` (if Salesforce CLI) · `@rules/splash.md` (if splash screen enabled in Phase 3) · `@rules/verification.md`. **Read `design-system.md` and `layout.md`** (no longer auto-imported) before producing any UI. Read `docs/specs/04-architect.md` — it is the locked contract this build follows.

Critical reminders:
- PEP 8 · type hints · docstrings · ruff + mypy clean.
- Error handling on all critical operations; `sys.excepthook` installed.
- Zero hardcoded visual value in Python — everything in `styles_*.qss` / `config.py`.
- Every styled widget has an `objectName` matching a QSS rule.
- No library that was not validated in Phase 1.

## Target directory

Use the project root chosen at the start of the flow (via `/python-app` or `/python-p1-scoping`). If it was not set in this flow, ask for it once:

Destination folder for the files? (e.g. C:\projects\MyApp)

Write all files there via `Write`. Create the needed subfolders before writing the files they contain.

## Anti-patterns — what NOT to do

- **Do not** deviate from `docs/specs/04-architect.md` silently — any structural change triggers the deviation protocol (stop, declare, validate) from `rules/mvc.md`.
- **Do not** use `QMessageBox` for business errors, `print()` for diagnostics, or hardcoded colors in Python.
- **Do not** write SQL outside `models/` or build a query by concatenation.
- **Do not** leave a `# TODO`, an unjustified `pass`, or a placeholder. Each batch is complete and self-contained.
- **Do not** introduce a library not validated in Phase 1.
- **Do not** mark the work done while `rules/verification.md §A` is failing.

## Delivery

- Announcement (in the user's language): `Batch N/[total] — [content]`
- Each file delivered as a complete, self-contained block via `Write`.
- Automatic chaining between batches without confirmation.
- Batch split: tables in `rules/mvc.md` (conditional on Phase 1 Q5 — tests or not, frozen in Phase 2).

## Verification

Apply `rules/verification.md` — both the executable commands (§A, blocking when the env is available) and the static integrity checks (§B, including the per-domain ones). Silent — reported only on a discrepancy. Cross-file checks run on the last batch.

## Last batch — mandatory deliverables

- **`main.py`** with the strict init order: `setup_logging()` → `run_migrations()` (if DB) → `QApplication` → `app.setStyle("Fusion")` → `app.setWindowIcon(...)` (if icon defined — `@rules/config.md`) → `install_translator(app)` (if i18n) → `create_splash(theme)` + `splash.show()` (if splash enabled) → `MainWindow` → `install_excepthook(window)` → `window.show()` → `QTimer.singleShot(SPLASH_MIN_DURATION_MS, lambda: splash.finish(window))` (if splash) → `app.exec()`. See `@rules/splash.md`.
- **Install instructions** (venv, pip, `python main.py`); pytest instructions appended if tests enabled.
- **`README.md`** written automatically at the project root: objective, features, out-of-scope, stack, architecture, installation, tests (if enabled), color palette.
- **`CLAUDE.md`** written at the generated project root (in the user's language), recording the app's identity for future sessions:

  ```markdown
  # [nom-app]

  ## Origin
  Framework: python v1.0.0

  ## Business context
  [What the app does — synthesized from docs/specs/02-featuring.md: objective + key features]

  ## Deviations from the framework
  - None
  ```
  `[nom-app]` = `APP_NAME`. The version is the one declared at the top of the framework `CLAUDE.md` (currently 1.0.0). Replace the `Deviations` list with every deviation validated via the Phase 4/5 deviation protocol (`- [deviation] — reason: [justification]`); if none, keep `- None`.
- **`.claude/settings.json`** written at the generated project root so the app stays self-enforced in later maintenance sessions:

  ```json
  {
    "permissions": {
      "allow": ["Bash(python:*)", "Bash(pip:*)", "Bash(pytest:*)", "Bash(ruff:*)", "Bash(mypy:*)", "Read", "Write", "Edit"],
      "deny": ["Read(**/.env)", "Write(**/.env)", "Write(**/.env.*)", "Edit(**/.env)", "Edit(**/.env.*)", "Write(**/secrets/**)", "Write(**/.venv/**)", "Write(**/__pycache__/**)", "Write(**/build/**)", "Write(**/dist/**)"]
    },
    "hooks": {
      "Stop": [{ "hooks": [{ "type": "command", "command": "ruff check ." }] }]
    }
  }
  ```
  The `Stop` hook runs the fast static check at the end of each turn; it assumes `ruff` is installed (`requirements-dev.txt`). Note in the README that the user can tune or remove it. **If the Salesforce CLI integration is on**, add `"Bash(sf:*)"` to the `allow` list (so maintenance sessions can verify flags with `sf <cmd> --help`).

## Splash screen — only if enabled in Phase 3

No dedicated batch. Deliver, per `@rules/splash.md`: `SPLASH_MIN_DURATION_MS` + `SPLASH_COLORS` in `config.py` (**Batch 1**), `views/splash_screen.py` (views batch), and the `main.py` orchestration (last batch — `create_splash` before `MainWindow`, `splash.finish(window)` after the min duration). Splash colors are a documented `config.py` exception (like `ICON_COLORS`), painted programmatically. If a splash icon path was provided in Phase 3, save it as `resources/icon.ico`. It counts toward the size, not a separate batch.

## Seed batch — only if DB ≠ none (Phase 1 Q2)

If a database was selected, deliver a standalone seed script `scripts/seed.py` that inserts a coherent demo dataset:
- Uses `models/db.py` (`get_connection()`) and the business models — never raw SQL outside `models/`.
- Coherent, FK-respecting data (~5-15 rows per entity), realistic values in the user's language, parents before children.
- Idempotent: insert only if the target tables are empty (count check first); re-running must not duplicate rows.
- Run instruction added to the README: `python scripts/seed.py`. Never called from `main.py`.

Announce `Batch [final]/[total] — scripts/seed.py` (before the tests batch if both apply). See `@rules/db.md`.

## Test batch — only if Phase 1 Q5 = Yes

Announce `Batch [final]/[total] — tests/ + requirements-dev.txt`. Deliver `tests/` mirroring the source structure (`@rules/tests.md`: mocked-controller pattern, qtbot smoke views, no `time.sleep`/`assert True`/network/prod-DB) + `requirements-dev.txt`, then append the pytest instructions to the README.

## Final delivery summary

Once the last batch (plus the seed/test batches if any) is delivered, close Phase 5 with a **delivery summary** in the user's language. **Make every file and the project folder a clickable Markdown link** `[label](path)`, each path pointing to the real on-disk location under the project root (relative to the project root, or absolute if the project root lies outside the current workspace). **Valid link syntax (mandatory)**: a Markdown link destination cannot contain spaces unless wrapped in angle brackets. When the path contains spaces (typical of absolute Windows paths), wrap the destination in `<…>` and use forward slashes, e.g. `[README.md](<D:/Documents/00 Mes Documents/.../my-app/README.md>)`. Without spaces, a plain relative path is fine. List:

- **Project folder** — the project root (clickable).
- **README.md** — how to run, stack, tree, conventions (clickable).
- **Generated `CLAUDE.md`** — the app identity for future sessions (clickable).
- **Documentation — phase specs** — one clickable link each: `docs/specs/01-scoping.md`, `docs/specs/02-featuring.md`, `docs/specs/03-designing.md`, `docs/specs/04-architect.md` (and the latest `docs/sessions/SESSION_*.md` if one exists).
- **How to run** — the key commands (also in the README):

  ```
  python -m venv .venv ; .venv\Scripts\activate
  pip install -r requirements.txt        # + -r requirements-dev.txt if tests
  python main.py
  ```
  (+ `python scripts/seed.py` if a DB was selected; `pytest` if tests enabled.)

The summary points to the documents; it does not restate them.

## Post-delivery adjustments

Isolated fix on the affected file + direct dependencies. Full rewrite via `Write` (never a partial diff).
After resolving an anomaly: cleanup report (`rules/mvc.md`) then offer `Do you want to remember this point? /python-save-memory`.
