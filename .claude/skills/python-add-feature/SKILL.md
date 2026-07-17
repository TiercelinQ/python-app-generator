---
name: python-add-feature
description: Add a feature to an existing project while respecting the locked architectural contract. Invoke from the target project root, after /python-load-project or on an already-loaded project.
model: sonnet
---

# /python-add-feature — Add a feature to a delivered project

## Role
Senior PySide6 developer working on an existing, contracted codebase.

## Goal
Add the requested feature end-to-end, contract-compliant, after an explicit contract-diff validation, without scope creep.

## Deliverable
The created/modified files on disk (one batch) + an updated `docs/specs/04-architect.md` if the structure changed.

---

## Prerequisite

The project must be loaded (`/python-load-project` run at session start, OR `docs/specs/04-architect.md` / README.md present and read).

If the project root has not been provided in this flow, first ask: `Project root? (folder path)`.

If no contract is known: stop and ask for `/python-load-project`.

## Step 1 — Light feature scoping

Ask the closed parameters with `AskUserQuestion` (clickable options, recommended first); the short description (Q1) stays free-form text:

New feature — a few questions:

1. Short description (1 sentence)
2. Business entity affected: [existing: list] | new (to name)
3. Type of change:
   A. New entity (model + view + controller)
   B. Extension of an existing entity
   C. New shared view (no new model)
   D. UI-only change (QSS or layout)
4. Generate tests for this feature? Yes / No (recommended: aligned with the project stack)

Mark a `(recommended)` option for each closed question, inferred from the existing project. If the request stays ambiguous (business rule, edge case), state assumptions explicitly and ask before the diff.

## Step 2 — Architectural contract diff

Produce (in the user's language):

## Contract diff — addition: [feature name]

### Created files
[list]

### Modified files
[list with nature: added method, added widget, added signal…]

### Created test files (if Q4 = Yes)
[mirror list]

### Impact on design-system / layout
[none | new component to respect within existing tokens]

→ Validation required before writing. Update `docs/specs/04-architect.md` once the diff is applied.

## Step 3 — Application — strict rules

- Read `design-system.md` and `layout.md` (no longer auto-imported) before any UI change. **Legacy design system**: if the app is on v1.x (README reference — see `/python-load-project` step 5), new UI follows the app's own v1.x conventions (its QSS sheets and existing widgets), never the framework's v2.0 files; the upgrade path is `/python-migrate-design`, on request.
- Fully respect `@rules/mvc.md`, `@rules/qss.md`, `@rules/errors.md`, `@rules/config.md`, `@rules/security.md`, `@rules/tests.md`, `@rules/logging.md`, `@rules/i18n.md`, `@rules/db.md`, `@rules/sf-cli.md` (if the Salesforce CLI integration is on), `@rules/versioning.md`, `@rules/verification.md`, `@rules/readme.md`. For an `sf`-related change, consult the matching `sf-cli-reference/` section file before writing any command/flag, and keep every `sf` call inside `models/sf_cli.py`.
- No modification not listed in the validated diff.
- No opportunistic improvement of adjacent code.
- DB migration needed → increment `DB_SCHEMA_VERSION`, add a `MIGRATIONS` entry in `models/migrations.py`.
- UI string added and i18n enabled → update the `.ts` (remind the user to run `scripts/i18n_update.ps1`).
- New styled widget → add a QSS rule in `styles_light.qss` AND `styles_dark.qss`.
- If the validated diff introduces a deviation from the contract, record it in the app's `CLAUDE.md` (`## Deviations from the framework`).

## Step 4 — Delivery

Single batch for the feature:

Feature [name] — [N files]

Deliver each created/modified file as a complete block. If tests requested: deliver in the same batch, at the end.

## Step 4b — Changelog entry

After the feature is delivered, append an entry under `## [Unreleased]` in `docs/release/CHANGELOG.md` (`@rules/versioning.md`) — **in English**, no version bump:
- `### Added` — the new capability, one concise line (add a `### Changed` line too if it alters existing behavior).
- If the change is backward-incompatible, mark it `**BREAKING:**` (drives a MAJOR at release).
- If `docs/release/CHANGELOG.md` is absent (app predates the system), skip silently and suggest `/python-load-project` to initialize it.

Do **not** bump the version — that happens at `/python-release`. Mention it once, at the end: the change is recorded under `[Unreleased]`; run `/python-release` when ready to cut a version.

## Step 5 — Anomaly

If the user reports an anomaly after delivery, apply the `@rules/mvc.md` cleanup protocol then offer `/python-save-memory`.

## Anti-patterns — what NOT to do
- **Do not** write anything not listed in the validated diff, or improve adjacent code.
- **Do not** add a DB column without bumping `DB_SCHEMA_VERSION` + a `MIGRATIONS` entry.
- **Do not** add a styled widget without rules in BOTH `styles_*.qss`.
- **Do not** exceed the contract silently — the diff + validation IS the protocol.

## Verification

Apply `@rules/verification.md`. Key points: all created/modified files match the validated diff; no import regression (existing files stay functional); if tests, `pytest` exit 0 on the **whole** project. Then apply `@rules/readme.md` — regenerate the README if the change touched a README-documented aspect.

## When the user asks something adjacent
- **"Just make it work, never mind the architecture"** → push back: the MVC split and the security rules are what keep the app safe and maintainable. Implement within them.
- **"Add a whole new screen/entity"** → that is a contract extension. Declare the new files/model in the diff, validate, then build.
- **"Fix this bug while you're here"** → if outside the current request scope, flag it and switch to `/python-fix-issue` rather than bundling an unrelated change.
