---
name: python-p2-featuring
description: Phase 2 of the development cycle — requirements analysis, calibration locked here, blocking validation before the layout, written to the analysis spec.
model: sonnet
---

# /python-p2-featuring — Requirements analysis

## Role
Requirements analyst — turn the scope into an unambiguous feature list and lock the sizing.

## Goal
Produce a structured requirements sheet, freeze the calibration, and get explicit sign-off before any layout work.

## Deliverable
`docs/specs/02-featuring.md` (written in French) + on-screen sheet.

---

## Instructions — Phase 2: Requirements analysis

Produce a structured sheet (in French), based on `docs/specs/01-scoping.md`:

## Analyse des besoins — [NOM_APP]

**Objectif**
[Description synthétique de l'application]

**Fonctionnalités retenues**
- [Fonctionnalité 1]
- [Fonctionnalité 2]
- …

**Hors périmètre**
- [Ce qui est explicitement exclu]

**Contraintes techniques**
- OS : Windows · PyQt6 · Python 3.10+
- DB : [valeur choisie en Phase 1]
- Préférences : [Oui/Non]
- i18n : [Oui/Non]
- Tests : [Oui/Non] — pytest + pytest-qt
- Packaging .exe : [Oui/Non] — PyInstaller
- Palette : [choix Phase 1 : nom ou custom, 5 rôles]

**Calibrage (figé après cette phase)**
- Fonctionnalités comptées : [N]
- Fichiers estimés : [N]
- Taille retenue : [Petit | Moyen / Grand]
- Lots : [N] (dont 1 lot tests si activé)

Apply the CALIBRATION table in `CLAUDE.md` (canonical source). **The calibration is confirmed here, from the real feature count.**

End with:

→ Validation requise avant Phase 3.
  Le calibrage est verrouillé dès validation.
  Confirmer ou lister les ajustements.

**Blocking rule**: do not move to Phase 3 until validation is explicit. If partial validation: list the open points, block until full resolution.

## Write the spec

Once validated, write the sheet to `docs/specs/02-featuring.md` (in French).

Chain to `/python-p3-designing` after validation.
