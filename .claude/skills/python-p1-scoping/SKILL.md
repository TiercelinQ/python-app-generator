---
name: python-p1-scoping
description: Phase 1 of the development cycle — scoping a new application (6 questions + full color palette choice), provisional calibration, and writing of the scoping spec.
model: sonnet
---

# /python-p1-scoping — Scoping

## Role
Project scoper — turn a vague idea into a bounded, validated scope.

## Goal
Lock the project parameters (DB, prefs, i18n, tests, packaging, palette) before any analysis.

## Deliverable
`docs/specs/01-scoping.md` (written in the user's language) + on-screen summary.

---

## Instructions — Phase 1: Scoping

> If invoked directly (not routed from `/python-app`) without a destination folder set for this flow, first ask: `Where to create the application? (destination folder path)`.

Ask the following 6 questions in **a single block** (in the user's language). Each closed question carries a `(recommended)` answer:

1. Application objective — free description.
2. Database: SQLite / PostgreSQL / JSON / CSV / none? (recommended: SQLite if structured data, otherwise none)
3. Persistent preferences between sessions (theme, window…)? Yes / No (recommended: Yes)
4. FR/EN internationalization for this project? Yes / No — FR by default (recommended: No unless a real EN need)
5. Automated tests (pytest + pytest-qt)? Yes / No (recommended: Yes for professional use)
6. .exe packaging (PyInstaller — build.spec + PowerShell script)? Yes / No (recommended: No unless distributing)

After receiving the answers, propose the **color palette**. A palette = 5 **light** roles (main background, secondary background, accent, text, details); the dark theme and all supporting tokens are derived (`design-system.md §2`).

Color palette for this project (5 roles, light theme — dark is derived):

A. Steel (default) — bg #FFFFFF · 2nd #F9FAFB · accent #4682B4 · text #111827 · details #E5E7EB — professional, tech, understated (recommended)
B. Forest — bg #FFFFFF · 2nd #F6F8F6 · accent #059669 · text #14201A · details #DCE5DF — natural, calm, fresh
C. Slate — bg #FFFFFF · 2nd #F8FAFC · accent #4F46E5 · text #1E293B · details #E2E8F0 — modern, crisp, indigo
D. Amber — bg #FFFDFB · 2nd #FBF6EF · accent #B45309 · text #1C1917 · details #ECE3D8 — warm, artisanal
E. Ruby — bg #FFFFFF · 2nd #FAF7F7 · accent #BE123C · text #1A1212 · details #EAE0E1 — bold, elegant

F. Custom palette — provide 5 light hex values: main background, secondary background, accent, text, details.

Palette rules (see `@rules/config.md` "Deriving the full palette" + `design-system.md §2`):

- Acier (default) is option A and the recommended default; the 4 other named palettes (B-E) and the custom option (F) are full palettes. The catalog values are canonical — do not improvise the named ones.
- From the 5 light roles, Claude **derives** and announces: supporting light tokens (`bg-muted`, `bg-elevated`, `text-subtle`, `text-muted`, `border-subtle`, `border-strong`), the 5 accent stops (`primary-50/400/700/800/900`), `onPrimary`, and the **whole dark theme** (lightness targets in `design-system.md §2`).
- Written to `styles_light.qss` + `styles_dark.qss` (neutrals) and `config.py` (`PRIMARY_*`, `ON_PRIMARY`, `ICON_COLORS`). Semantic colors stay fixed.
- **Contrast check (WCAG AA, non-blocking)**: compute text/bg, text-subtle/bg, accent/bg, onPrimary/accent; if a ratio fails AA, report it (`couleur — ratio — cible`) and ask the user to confirm or adjust before continuing.
- The global `design-system.md` stays unchanged. If A or no answer: default palette (values already known).

Then announce the **provisional** calibration:

Provisional calibration: [Small | Medium/Large] — [N] batches (incl. 1 test batch if enabled)
(Confirmed at the end of Phase 2, after counting the real features.)

Apply the CALIBRATION table in `CLAUDE.md` (canonical source).

## Write the spec

Write `docs/specs/01-scoping.md` (in the user's language) capturing: objective, DB, preferences, i18n, tests, packaging, the **palette** (name or custom; the 5 light roles + the derived dark theme + accent stops + onPrimary; semantic kept fixed) and the contrast-check result, validated libraries, and the provisional calibration. If `docs/specs/` does not exist yet, create it (it will live in the generated project root).

Chain immediately to Phase 2 (`/python-p2-featuring`).
