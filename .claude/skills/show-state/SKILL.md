---
name: show-state
description: Show the current state of the in-progress project (phase, batch, locked decisions, open points).
model: haiku
---

# /show-state — Current state

## Role
Status reporter.

## Goal
Give a one-glance state of the project.

## Deliverable
The status block (French).

---

Show exactly this format (in French):

```
Phase : [nom] | Lot : [X/total] | Prochain : [action attendue]
Décisions verrouillées : [liste]
Points ouverts : [liste ou "aucun"]
```

If no project is active: "Aucun projet actif. Taper /python-app pour démarrer."

Do not append the `/session · /show-state · /show-contract` reminder after this reply.
