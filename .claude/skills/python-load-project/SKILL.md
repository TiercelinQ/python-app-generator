---
name: python-load-project
description: Load an existing Python/PySide6 project (Phase 5 complete) from its specs and README — bring the generator rules to bear on already-delivered code. Invoke from the target project root before any intervention.
model: sonnet
---

# /python-load-project — Load an existing project

## Role
Onboarding analyst — take charge of a delivered codebase under the generator rules.

## Goal
Understand the project's structure and confirm the rules apply to any later change.

## Deliverable
A one-block confirmation (in the user's language) of the loaded project.

---

> If the project root has not been provided in this flow, first ask: `Project root to load? (folder path)`. Read everything below relative to that root.

Use the native Claude Code tools (Windows-compatible):

1. **Read the source of truth in priority order:**
   - `docs/specs/04-architect.md` (locked contract — most reliable). If present, it is authoritative for the structure.
   - Other `docs/specs/*` for the scoping/analysis/layout decisions.
   - `README.md` at the root. If both specs and README are absent: offer `/python-generate-readme` and stop.
2. **Detect `tests/`** via `Glob` with the pattern `tests/**/*.py` → count the files for the Tests line.
3. Read `config.py` + walk the source to confirm the MVC structure (models / views / controllers / utils).
4. Confirm take-over with this exact format (in the user's language):

Project loaded: [APP_NAME] v[VERSION]

Stack : Python [v] · PySide6
DB : [value]
Entities detected: [list]
Tests : [present ([N] files) | absent]
Salesforce CLI: [enabled (sf v2 runner) | disabled]
Design system: [v2.0 | v1.x (legacy)]
Specs: [docs/specs present: yes/no]

Generator rules applied. Ready for: development · fixes · improvements · adjustments.

5. **Design system version check.** Read the design-system version the app's `README.md` references (every generated app records it); confirm with legacy markers if needed (`qtawesome` in `requirements.txt`/imports, `border-radius: 0` era sheets without `resources/icons/`). If the app is on **v1.x** and its README carries no "v2.0 conversion declined" note, propose **once**, right after the confirmation block: convert to v2.0 with `/python-migrate-design` (recommended). If the user declines, append `(v2.0 conversion declined on [date])` to the README's design-system reference line and do not re-propose — only on explicit request. **A v1.x app is maintained in its own v1.x conventions** (its QSS sheets, `config.py` colors, and existing code are the visual reference); never mix v2.0 visuals into it.
6. Read and apply all rules (`CLAUDE.md`, `@rules/mvc.md` · `@rules/qss.md` · `@rules/errors.md` · `@rules/config.md` · `@rules/security.md` · `@rules/logging.md` · `@rules/tests.md` (if tests present) · `@rules/sf-cli.md` (if the project has the Salesforce integration) · `@rules/verification.md`, `design-system.md`, `layout.md`) to any later change. The `rules/*` are not auto-imported: read them before any code change. On a v1.x app (step 5), the app's own design system version wins over the framework's `design-system.md` for visual conventions.
7. Any structural or security deviation detected between the code and the rules (or vs `docs/specs/04-architect.md`): report it, do not fix without a request (hand off to `/python-fix-issue` or `/python-refactor-code`).
