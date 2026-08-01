# Changelog

All notable changes to this generator are documented in this file.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.
(This is the changelog of the **generator** itself, distinct from the `docs/release/CHANGELOG.md` of each generated app.)

## [1.5.0] - 2026-08-01
### Added
- Single-instance lock: `QLockFile` acquired in `main.py` (after `setup_logging()`, before `run_migrations()`) when the app writes data; a second instance logs, prints a one-line message, and exits without touching any file (`rules/security.md §4`).
- `pip-audit` mentioned in the last batch instructions (PyPA dependency-vulnerability check — parity with `npm audit` on the npm stacks, `rules/security.md §6`).
- Phase 5 offers `/python-save-session` between batches when the session is running long or the context is heavily loaded (safety net before saturation; automatic chaining stays the default).
- Phase 2 Step 1 constrains the application name: space-free candidates, a free-typed name is normalized into the technical identifier (`APP_NAME`); the display name (window title, README) may keep spaces and both are recorded when they differ.
- `/python-release` now updates the README title line (`# [APP_NAME] — v[NEW]`) as a targeted edit of that single line; the version-bump trigger is documented in `rules/readme.md`.
- The app-template `.claude/settings.json` deny anchoring is documented as deliberate in Phase 5 ("Deny anchoring" note — no deny may match `docs/release/CHANGELOG.md`).

### Changed
- Phase 5 loads `tests.md` / `i18n.md` / `db.md` only when the matching option is enabled (leaner context on projects without tests/i18n/DB).
- The seed script `scripts/seed.py` ships inside the last code batch — no dedicated seed batch; the announced batch total now always matches the frozen calibration.
- Downstream Phase 1 question numbers removed: conditions now read "if [option] enabled in Phase 1"; the numbers stay in `p1-scoping` only.
- The debug env var name is normalized (`[^A-Z0-9]` → `_`) in `rules/logging.md`, so a hyphenated app name stays shell-usable.
- The CALIBRATION closing paragraph is harmonized across the 5 generators ("the highest criterion wins"; "Salesforce and splash push the size up").

## [1.4.0] - 2026-07-26
### Added
- Phase 5 now writes the delivery baseline session file `docs/sessions/SESSION_<App>_S0.md` automatically at the end of the last batch (`/python-save-session` template, `N = 0`, overwritten if Phase 5 is replayed). Manual `/python-save-session` saves keep numbering from `S1`. The delivery summary links it.

## [1.3.0] - 2026-07-25
### Added
- Generated apps now ship a `.gitignore` at the project root (delivered in the last batch): Python bytecode/build/env outputs (`__pycache__/`, `.venv/`, `/dist/`, `/build/`, `*.egg-info/`, `.env`), Claude Code personal files (`settings.local.json`, `agent-memory/`), `tasks/`, and the private `docs/specs/` — while keeping `docs/release/CHANGELOG.md`, `.claude/settings.json`, the generated `CLAUDE.md`, `tests/`, and `scripts/` tracked. New `## .gitignore` section in `rules/config.md`, a last-batch check in `rules/verification.md`, and a deliverable in `p5-development`.

### Changed
- The generated app `README.md` is now always written in English (public-facing document), regardless of the user's interface language; specs under `docs/specs/` stay in the user's language. New `Language — English` section in `rules/readme.md`, write-point note in `generate-readme`, corrected parenthesis in `rules/versioning.md`.

## [1.2.0] - 2026-07-18
### Added
- Data table (QTableView) columns are sortable ascending and descending (`setSortingEnabled(True)` + native header indicator).
- Main window is centered on the primary screen at launch; a saved window position (restore-position preference) takes precedence.
- Post-delivery reminder: the Phase 5 delivery summary and the generated app `CLAUDE.md` now list the maintenance commands and `/python-release`.

### Changed
- Sidebar (P2) labels word-wrap within the fixed 240px width instead of eliding.
- Phase 1 Salesforce CLI question is shown only when the objective mentions Salesforce (otherwise off, still enabled on explicit request).

## [1.1.0] - 2026-07-17
### Added
- App changelog + SemVer versioning system for generated apps: new `rules/versioning.md`, new `/python-release` skill, and a seeded `docs/release/CHANGELOG.md` (Keep a Changelog, English).
- Maintenance skills (`add-feature`, `fix-issue`, `refactor-code`, `migrate-design`) now record their change under `## [Unreleased]`; `/python-load-project` offers to initialize the changelog retroactively on a legacy app.

### Changed
- `CLAUDE.md`, `p5-development`, `verification.md`, `python-app`, `show-state` updated for the versioning system.

## [1.0.0]
- Unified edition baseline: 5-phase generation pipeline (p1 scoping to p5 development), calibration, strict MVC contract, error contract (named exceptions, toasts), Python/PySide6 security rules, design system v2.0 (depth by stroke, vendored Lucide SVGs), Salesforce `sf` v2 integration, and the maintenance skill set.
