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

Present the start menu with the `AskUserQuestion` tool (single question, 4 clickable options — do not make the user type a number):
- New application
- Resume a session (SESSION file)
- Load an existing project (Phase 5 complete)
- Maintain a delivered project (add / fix / analyze)

Map the chosen option to the routing below. The folder/SESSION-path prompts stay free-form text.

Routing:

- `1` → chain directly to `/python-p1-scoping`, which handles the project folder name, location, and creation (the project root is established there).
- `2` → ask for the SESSION file path:
  Provide the path to your SESSION file:
  (e.g. C:\projects\my-app\docs\sessions\SESSION_MyApp_S1.md)
  Read the file via the native `Read` tool (never `cat` — Windows-compatible). The project root is the folder containing `docs/` (two levels up from the SESSION file); confirm it before resuming, then invoke `/python-save-session` for the resume.
- `3` → ask for the project root to load, then invoke `/python-load-project` (`.claude/` present at that root):
  Project root to load? (folder path, e.g. C:\projects\MyApp)
- `4` → ask for the project root, ensure the project is loaded (`/python-load-project` if not already), then route by intent:
  Project root to maintain? (folder path, e.g. C:\projects\MyApp)
  - add a feature → `/python-add-feature`
  - understand / trace how something works → `/python-trace-feature`
  - fix a bug → `/python-fix-issue`
  - restructure existing code → `/python-refactor-code`
  - verify the build / run checks → `/python-run-tests`

If typed mid-project: show the menu only, without resetting the context.
