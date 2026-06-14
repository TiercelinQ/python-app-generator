---
name: phase5-developpement
description: Phase 5 of the development cycle — batch code delivery, files written directly to disk, executable verification, final README. Invoke after the architectural contract (Phase 4) is validated, and for each subsequent batch.
model: sonnet
---

# /phase5-developpement — Batch development

## Role
Senior PyQt6 developer — build the contracted app to a clean, runnable state.

## Goal
Deliver the application in batches, each one ruff/mypy-clean and contract-compliant, ending with install instructions and a README.

## Deliverable
The full project source on disk + `README.md` + verified build.

---

## Code rules

Apply fully: `@rules/mvc.md` · `@rules/qss.md` · `@rules/errors.md` · `@rules/config.md` · `@rules/security.md` · `@rules/tests.md` · `@rules/logging.md` · `@rules/i18n.md` · `@rules/db.md` · `@rules/verification.md`. **Read `design-system.md` and `layout.md`** (no longer auto-imported) before producing any UI. Read `docs/specs/04-contrat.md` — it is the locked contract this build follows.

Critical reminders:
- PEP 8 · type hints · docstrings · ruff + mypy clean.
- Error handling on all critical operations; `sys.excepthook` installed.
- Zero hardcoded visual value in Python — everything in `styles_*.qss` / `config.py`.
- Every styled widget has an `objectName` matching a QSS rule.
- No library that was not validated in Phase 1.

## Target directory

At the start of Phase 5, ask for the target project root directory:

```
Répertoire de destination pour les fichiers ? (ex: C:\projets\MonApp)
```

Store this path. Write all files there via `Write`. Create the needed subfolders before writing the files they contain.

## Anti-patterns — what NOT to do

- **Do not** deviate from `docs/specs/04-contrat.md` silently — any structural change triggers the deviation protocol (stop, declare, validate) from `rules/mvc.md`.
- **Do not** use `QMessageBox` for business errors, `print()` for diagnostics, or hardcoded colors in Python.
- **Do not** write SQL outside `models/` or build a query by concatenation.
- **Do not** leave a `# TODO`, an unjustified `pass`, or a placeholder. Each batch is complete and self-contained.
- **Do not** introduce a library not validated in Phase 1.
- **Do not** mark the work done while `rules/verification.md §A` is failing.

## Delivery

- Announcement (French): `Lot N/[total] — [content]`
- Each file delivered as a complete, self-contained block via `Write`.
- Automatic chaining between batches without confirmation.
- Batch split: tables in `rules/mvc.md` (conditional on Phase 1 Q5 — tests or not, frozen in Phase 2).

## Verification

Apply `rules/verification.md` — both the executable commands (§A, blocking when the env is available) and the static integrity checks (§B, including the per-domain ones). Silent — reported only on a discrepancy. Cross-file checks run on the last batch.

## Last batch — mandatory deliverables

- **`main.py`** with the strict init order: `setup_logging()` → `run_migrations()` (if DB) → `QApplication` → `install_translator(app)` (if i18n) → `MainWindow` → `install_excepthook(window)` → `window.show()` → `app.exec()`.
- **Install instructions** (venv, pip, `python main.py`); pytest instructions appended if tests enabled.
- **`README.md`** written automatically at the project root: objective, features, out-of-scope, stack, architecture, installation, tests (if enabled), primary color.
- **`CLAUDE.md`** written at the generated project root (in French), recording the app's identity for future sessions:

  ```markdown
  # [nom-app]

  ## Origine
  Framework : python v1.0.0

  ## Contexte métier
  [Ce que fait l'app — synthèse issue de docs/specs/02-analyse.md : objectif + fonctionnalités clés]

  ## Écarts par rapport au framework
  - Aucun
  ```
  `[nom-app]` = `APP_NAME`. The version is the one declared at the top of the framework `CLAUDE.md` (currently 1.0.0). Replace the `Écarts` list with every deviation validated via the Phase 4/5 deviation protocol (`- [écart] — raison : [justification]`); if none, keep `- Aucun`.
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
  The `Stop` hook runs the fast static check at the end of each turn; it assumes `ruff` is installed (`requirements-dev.txt`). Note in the README that the user can tune or remove it.

## Test batch — only if Phase 1 Q5 = Yes

Announce `Lot [final]/[total] — tests/ + requirements-dev.txt`. Deliver `tests/` mirroring the source structure (`@rules/tests.md`: mocked-controller pattern, qtbot smoke views, no `time.sleep`/`assert True`/network/prod-DB) + `requirements-dev.txt`, then append the pytest instructions to the README.

## Post-delivery adjustments

Isolated fix on the affected file + direct dependencies. Full rewrite via `Write` (never a partial diff).
After resolving an anomaly: cleanup report (`rules/mvc.md`) then offer `Veux-tu mémoriser ce point ? /memoriser`.
