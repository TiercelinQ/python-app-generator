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
`docs/specs/02-featuring.md` (written in the user's language) + on-screen sheet.

---

## Instructions — Phase 2: Requirements analysis

Produce a structured sheet (in the user's language), based on `docs/specs/01-scoping.md`:

## Requirements analysis — [NOM_APP]

**Objective**
[Concise description of the application]

**Selected features**
- [Feature 1]
- [Feature 2]
- …

**Out of scope**
- [What is explicitly excluded]

**Technical constraints**
- OS: Windows · PyQt6 · Python 3.10+
- DB: [value chosen in Phase 1]
- Preferences: [Yes/No]
- i18n: [Yes/No]
- Tests: [Yes/No] — pytest + pytest-qt
- .exe packaging: [Yes/No] — PyInstaller
- Palette: [Phase 1 choice: name or custom, 5 roles]

**Calibration (frozen after this phase)**
- Counted features: [N]
- Estimated files: [N]
- Chosen size: [Small | Medium / Large]
- Batches: [N] (incl. 1 test batch if enabled)

Apply the CALIBRATION table in `CLAUDE.md` (canonical source). **The calibration is confirmed here, from the real feature count.**

End with:

→ Validation required before Phase 3.
  The calibration is locked upon validation.
  Confirm or list the adjustments.

**Blocking rule**: do not move to Phase 3 until validation is explicit. If partial validation: list the open points, block until full resolution.

## Write the spec

Once validated, write the sheet to `docs/specs/02-featuring.md` (in the user's language).

Chain to `/python-p3-designing` after validation.
