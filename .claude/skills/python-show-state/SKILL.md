---
name: python-show-state
description: Show the current state of the in-progress project (phase, batch, locked decisions, open points).
model: haiku
---

# /python-show-state — Current state

## Role
Status reporter.

## Goal
Give a one-glance state of the project.

## Deliverable
The status block (in the user's language).

---

Show exactly this format (in the user's language):

Phase: [name] | Batch: [X/total] | Next: [expected action]
Locked decisions: [list]
Open points: [list or "none"]

If no project is active: "No active project. Type /python-app to start."

Do not append the `/python-save-session · /python-show-state · /python-show-contract` reminder after this reply.
