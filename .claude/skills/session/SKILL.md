---
name: session
description: Generate the session save file to resume the project later, referencing the specs. Invoke at the end of a session.
model: haiku
---

# /session — Session save

## Role
Session archivist.

## Goal
Persist enough state to resume the project exactly where it stopped.

## Deliverable
`claude-sessions/SESSION_[app_name]_S[N].md` (French).

---

Use the native Claude Code tools (Windows-compatible):

1. **Create** the `claude-sessions/` folder if it does not exist (PowerShell: `New-Item -ItemType Directory -Force -Path claude-sessions | Out-Null`).
2. Determine `[N]`: list `claude-sessions/SESSION_*_S*.md` via `Glob`, extract the integers (`S(\d+)\.md$`), `[N] = max + 1` (or `1` if none). `[app_name]` = exact `APP_NAME` from `config.py` (no spaces).
3. **Write** `claude-sessions/SESSION_[app_name]_S[N].md` via `Write`:

```markdown
# SESSION_S[N] — [NOM_APP] · [Phase terminée]

## Statut

Phase terminée : [N — nom]
Phase suivante : [N+1 — nom]
Lot suivant : [X+1/total] (si Phase 5)

## Décisions verrouillées

- OS : Windows · Framework : PyQt6
- DB : [valeur] · Préférences : [Oui/Non] · i18n : [Oui/Non] · Tests : [Oui/Non] · Packaging : [Oui/Non]
- Couleur primaire : [choix + hex]
- Calibrage : [N] lots (dont 1 lot tests si activé)
- Fonctionnalités retenues : [liste]
- Hors périmètre : [liste]
- Layout retenu : [description]

## Specs

Référence : docs/specs/01-cadrage.md · 02-analyse.md · 03-layout.md · 04-contrat.md
(le contrat verrouillé dans 04-contrat.md fait foi — ne pas le dupliquer ici)

## Lots livrés

- [x] Lot 1 — [contenu]
- [ ] Lot 2 — [contenu]
- ...

## Points ouverts

[liste ou "aucun"]
```

> If `docs/specs/04-contrat.md` exists, reference it instead of duplicating the full tree. Only summarize the locked decisions here.

4. Confirm:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 SAUVEGARDE SESSION
Fichier écrit : claude-sessions/SESSION_[nom_app]_S[N].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Do not append the `/session · /statut · /contrat` reminder after this reply.

## Resume from a SESSION file

If the message contains a SESSION block (or the user gives a path):
1. **Read** the file via `Read`.
2. Reply: `📋 Reprise [NOM_APP] — [Phase suivante] | Lot [X/total] | Points ouverts : [liste ou "aucun"]`
3. Chain immediately without re-asking resolved questions; invoke the skill for the next phase.
