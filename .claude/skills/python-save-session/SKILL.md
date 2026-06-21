---
name: python-save-session
description: Generate the session save file to resume the project later, referencing the specs. Invoke at the end of a session.
model: haiku
---

# /python-save-session — Session save

## Role

Session archivist.

## Goal

Persist enough state to resume the project exactly where it stopped.

## Deliverable

`docs/sessions/SESSION_[app_name]_S[N].md` (in the user's language).

---

Use the native Claude Code tools (Windows-compatible):

1. **Create** the `docs/sessions/` folder if it does not exist (PowerShell: `New-Item -ItemType Directory -Force -Path docs/sessions | Out-Null`).
2. Determine `[N]`: list `docs/sessions/SESSION_*_S*.md` via `Glob`, extract the integers (`S(\d+)\.md$`), `[N] = max + 1` (or `1` if none). `[app_name]` = exact `APP_NAME` from `config.py` (no spaces).
3. **Write** `docs/sessions/SESSION_[app_name]_S[N].md` via `Write`:

# SESSION_S[N] — [APP_NAME] · [completed phase]

## Status

Completed phase: [N — name]
Next phase: [N+1 — name]
Next batch: [X+1/total] (if Phase 5)

## Locked decisions

- OS: Windows · Framework: PyQt6
- DB: [value] · Preferences: [Yes/No] · i18n: [Yes/No] · Tests: [Yes/No] · Packaging: [Yes/No]
- Palette: [name or custom; 5 light roles + derived]
- Calibration: [N] batches (incl. 1 test batch if enabled)
- Selected features: [list]
- Out of scope: [list]
- Chosen layout: [description]

## Specs

Reference: docs/specs/01-scoping.md · 02-featuring.md · 03-designing.md · 04-architect.md
(the locked contract in 04-architect.md is authoritative — do not duplicate it here)

## Delivered batches

- [x] Batch 1 — [content]
- [ ] Batch 2 — [content]
- ...

## Open points

[list or "none"]

> If `docs/specs/04-architect.md` exists, reference it instead of duplicating the full tree. Only summarize the locked decisions here.

4. Confirm:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SESSION SAVE
File written: docs/sessions/SESSION\_[app_name]\_S[N].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Do not append the `/python-save-session` · `/python-show-state` · `/python-show-contract` reminder after this reply.

## Resume from a SESSION file

If the message contains a SESSION block (or the user gives a path):

1. **Read** the file via `Read`.
2. Reply: `Resuming [NOM_APP] — [next phase] | Batch [X/total] | Open points: [list or "none"]`
3. Chain immediately without re-asking resolved questions; invoke the skill for the next phase.
