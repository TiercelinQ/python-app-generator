# README synchronization rule

> The generated app's `README.md` is a **derived** document — its source of truth is the code plus `docs/specs/04-architect.md`. After any post-delivery change, the README must keep reflecting what shipped. This is the single, shared definition of when and how to refresh it. Referenced by `/python-add-feature`, `/python-fix-issue`, `/python-refactor-code`.

## What the README documents

objective · stack & dependencies · file tree · MVC modules (models/views/controllers) · DB schema · conventions · build & run. Exact sections: `/python-generate-readme`.

## When to refresh (trigger)

Regenerate the README **iff** the change touched a documented aspect above:
- a dependency added/removed (`requirements.txt`), or a stack change,
- the file tree changed (a model/view/controller/module added, renamed, moved, or deleted),
- the DB schema changed (table, column, `DB_SCHEMA_VERSION`/migration),
- build or run steps changed (packaging, scripts).

A purely internal change (a private method, the body of an existing controller, a QSS token value, a bug fix with no structural impact) does **not** trigger a refresh.

## How to refresh

Regenerate the README via the logic of `/python-generate-readme` (reads specs + code), in the same delivery, without asking. Full regeneration — the README is derived, so hand edits are not preserved. No manual "offer" step.

## Read-only skills

Verification/analysis skills (`/python-run-tests`, `/python-trace-feature`) never rewrite the README. At most they flag it as stale; refreshing is done by the write skills above.
