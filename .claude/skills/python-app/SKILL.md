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

- `1` → ask for the destination folder, then chain to `/p1-scoping`:
  ```
  Où créer l'application ? (chemin du dossier de destination, ex: C:\projets\MonApp)
  ```
  Store this path as the project root — all generated files and specs (`docs/specs/`) are written there.
- `2` → ask for the SESSION file path:
  ```
  Indique le chemin vers ton fichier SESSION :
  (ex: C:\projets\mon-app\docs\sessions\SESSION_MonApp_S1.md)
  ```
  Read the file via the native `Read` tool (never `cat` — Windows-compatible). The project root is the folder containing `docs/` (two levels up from the SESSION file); confirm it before resuming, then invoke `/save-session` for the resume.
- `3` → ask for the project root to load, then invoke `/load-project` (`.claude/` present at that root):
  ```
  Racine du projet à charger ? (chemin du dossier, ex: C:\projets\MonApp)
  ```
- `4` → ask for the project root, ensure the project is loaded (`/load-project` if not already), then route by intent:
  ```
  Racine du projet à maintenir ? (chemin du dossier, ex: C:\projets\MonApp)
  ```
  - add a feature → `/add-feature`
  - understand / trace how something works → `/trace-feature`
  - fix a bug → `/fix-issue`
  - restructure existing code → `/refactor-code`
  - verify the build / run checks → `/run-tests`

If typed mid-project: show the menu only, without resetting the context.
