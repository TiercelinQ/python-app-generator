# Verification rules — single source of truth

> Centralized, reusable verification for the whole framework. Referenced by `/p5-development`, `/feature-add`, `/fix`, and `/test` — never duplicated in those skills.
> Two parts: **executable verification** (run real commands) and **static integrity** (read the code). Run silently; report only on a discrepancy.

---

## A. Executable verification (run the commands)

When the environment allows it (Python + venv available), these commands are **mandatory** and a failure is **blocking** — do not mark work as done while any of them fails. Run them in order:

```
python -m venv .venv ; .venv\Scripts\activate    # Windows
pip install -r requirements.txt                  # + requirements-dev.txt if tests/tooling
ruff check .                                      # lint — clean
ruff format --check .                             # format — clean
mypy .                                            # type-check (strict) — clean
pytest                                            # ONLY if tests enabled (Phase 1 Q5 = Yes) — exit code 0
python main.py                                    # smoke launch (manual — confirm no startup crash)
```

Rules:
- A non-zero exit or any reported error is a failure → fix the root cause, do not silence the rule. Re-run until clean.
- **`pytest`**: run only if `tests/` exists (Phase 1 Q5 = Yes). **Do not create a test suite if the project has none** — the default verification is ruff + mypy + smoke launch.
- `ruff`/`mypy` available via `requirements-dev.txt`; if absent, install them or fall back to the static read-through and tell the user.
- If Python/venv is **not** available in the environment, say so explicitly, fall back to the static checks below, and list the commands the user must run themselves. Never claim a clean type-check you could not run.
- Quote the relevant command output as proof when reporting completion.
- The generated app ships a `.claude/settings.json` (deny guards on secrets/artifacts + a `Stop` hook running `ruff check .`). These enforce the rules automatically in later maintenance sessions but **do not replace** this checklist.

---

## B. Static integrity (read the code)

### Every batch / every change
1. Valid Python syntax.
2. Imports: all used, none missing, MVC separation respected (Controller → Model + View; never Model → View).
3. MVC responsibilities respected (zero business logic in view/controller, zero UI in model). See `rules/mvc.md` anti-patterns.
4. Zero `# TODO`, zero unjustified `pass`, zero unjustified `any`/untyped public API.
5. Python 3.10+ · PyQt6 stable · zero PyQt5 API.
6. `design-system.md` and `layout.md` compliance — zero hardcoded visual value in Python, every styled widget has an `objectName`. See `rules/qss.md` anti-patterns.
7. Errors: business exceptions raised in models, caught in controllers, surfaced via `show_toast`; no `QMessageBox`/inline banner; `sys.excepthook` installed. See `rules/errors.md`.
8. Security: no hardcoded secret; SQL 100% parameterized; user paths resolved + bounded; no `shell=True`/`eval`/`exec` on untrusted input. See `rules/security.md`.

### Last batch only — cross-file
8. All inter-layer imports resolved.
9. Signals/slots consistent (every connected signal has a slot, every slot is connected).
10. Architectural contract (`docs/specs/04-architect.md`) respected — every file matches the locked contract, or a declared+validated deviation exists.
11. Zero hardcoded visual value in Python; `README.md` generated and complete.

### Per-domain (conditional — see the matching rule for detail)
- **DB** (`rules/db.md`): `models/db.py` + `models/migrations.py` present and called in `main.py` before the MainWindow; `config.DB_SCHEMA_VERSION` == `max(MIGRATIONS.keys())`; no `connect` outside `db.py`; SQL 100% parameterized.
- **i18n** (`rules/i18n.md`): `resources/i18n/app_{fr,en}.{ts,qm}` present; no hardcoded French string in `views/`; `QTranslator` installed before the MainWindow.
- **logging** (`rules/logging.md`): `utils/logger.py` conforming; `setup_logging()` first line of `main.py`; no `print(` in source folders; non-re-raising `except` calls `logger.exception(...)`.
- **tests** (`rules/tests.md`): each source module has its matching test file (Phase 4 mapping); `pytest` exit 0; `requirements-dev.txt` present.

---

## C. Reporting

- All clean → one short confirmation line in French (no full recap of the checklist).
- Any discrepancy → name the file, the failing check (§A command output or §B item number), and the fix applied or proposed.
- Verification that could not be run (no env) → state it plainly and list the commands the user must run.
