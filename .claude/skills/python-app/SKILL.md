---
name: python-app
description: Start menu of the Python/PyQt6 app generator — new app, resume a session, load a delivered project, or maintain one. Invoke to start or resume a project.
model: haiku
---

# /python-app — Start / resume / maintenance menu

## Role
Entry-point dispatcher for the Python app generator.

## Goal
Route the user to the right flow without re-asking resolved questions.

## Deliverable
The menu, then a handoff to the selected skill.

---

Show exactly this menu (in French):

```
Que faire ?

1. Nouvelle application
2. Reprendre une session (fichier SESSION)
3. Charger un projet existant (Phase 5 terminée)
4. Maintenir un projet livré (ajouter / corriger / analyser)

→ Réponds 1, 2, 3 ou 4.
```

Routing:

- `1` → chain immediately to `/phase1-cadrage`.
- `2` → ask for the SESSION file path:
  ```
  Indique le chemin vers ton fichier SESSION :
  (ex: C:\projets\mon-app\claude-sessions\SESSION_MonApp_S1.md)
  ```
  Read the file via the native `Read` tool (never `cat` — Windows-compatible), then invoke `/session` for the resume.
- `3` → invoke `/charger-projet` (from the target project root, `.claude/` present).
- `4` → ensure the project is loaded (`/charger-projet` if not already), then route by intent:
  - add a feature → `/feature-add`
  - understand / trace how something works → `/analyze`
  - fix a bug → `/fix`
  - restructure existing code → `/refactor`
  - verify the build / run checks → `/test`

If typed mid-project: show the menu only, without resetting the context.
