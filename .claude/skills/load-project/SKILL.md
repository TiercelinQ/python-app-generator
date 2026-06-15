---
name: load-project
description: Load an existing Python/PyQt6 project (Phase 5 complete) from its specs and README — bring the generator rules to bear on already-delivered code. Invoke from the target project root before any intervention.
model: haiku
---

# /load-project — Load an existing project

## Role
Onboarding analyst — take charge of a delivered codebase under the generator rules.

## Goal
Understand the project's structure and confirm the rules apply to any later change.

## Deliverable
A one-block confirmation (French) of the loaded project.

---

> If the project root has not been provided in this flow, first ask: `Racine du projet à charger ? (chemin du dossier)`. Read everything below relative to that root.

Use the native Claude Code tools (Windows-compatible):

1. **Read the source of truth in priority order:**
   - `docs/specs/04-architect.md` (locked contract — most reliable). If present, it is authoritative for the structure.
   - Other `docs/specs/*` for the scoping/analysis/layout decisions.
   - `README.md` at the root. If both specs and README are absent: offer `/generate-readme` and stop.
2. **Detect `tests/`** via `Glob` with the pattern `tests/**/*.py` → count the files for `[N]`.
3. Read `config.py` + walk the source to confirm the MVC structure.

Confirm take-over with this exact format (in French):

```
Projet [NOM_APP] v[VERSION] chargé.

Stack    : [résumé une ligne]
DB       : [valeur]
Fonctionnalités : [N] — [liste courte]
Architecture    : [N] fichiers — MVC PyQt6
Tests    : [présents ([N] fichiers) | absents]
Specs    : [docs/specs présent : oui/non]

Prêt pour : développement · corrections · améliorations · ajustements.
```

Immediately apply all the `CLAUDE.md` rules to any intervention on this project: strict MVC, QSS only, toasts, `design-system.md`, `layout.md`, `tests.md` if tests present. The `rules/*` are not auto-imported: read them before any code change. Any structural deviation detected between the code and the rules (or vs `docs/specs/04-architect.md`): report it, do not fix without a request (hand off to `/fix` or `/refactor`).
