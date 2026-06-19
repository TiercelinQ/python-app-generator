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

Ask Q1 (objective) as free-form text, then the closed parameters with the `AskUserQuestion` tool (clickable options, the recommended one first / marked `(recommended)`). The tool caps at **4 questions per call**, so split the closed parameters into **two calls**.

1. **Objective** — free-form text: "Application objective? (free description)".
2. **`AskUserQuestion` — call 1** (4 questions, each with a recommended option):
   - **Database**: `SQLite` (recommended, if structured data) · `JSON` · `CSV` · `none`. PostgreSQL via the **Other** option.
   - **Persistent preferences** (theme, window…): `Yes` (recommended) · `No`.
   - **FR/EN i18n** (FR by default): `No` (recommended, unless a real EN need) · `Yes`.
   - **Automated tests** (pytest + pytest-qt): `Yes` (recommended, pro use) · `No`.
3. **`AskUserQuestion` — call 2** (1 question):
   - **.exe packaging** (PyInstaller — build.spec + PowerShell script): `No` (recommended, unless distributing) · `Yes`.

After the answers, propose the **color palette** with `AskUserQuestion` (single question; clickable options from the catalog, recommended default first; the **Other** option covers a remaining named palette and the custom palette). A palette = 5 **light** roles (main background, secondary background, accent, text, details); the dark theme and all supporting tokens are derived (`design-system.md §2`).

- **Palette — `AskUserQuestion`**, options (≤ 4): `Steel` (default, recommended) · `Forest` · `Slate` · `Amber`. The **Other** option covers `Ruby` and a **custom palette**. If the user picks a custom palette, ask the 5 light hex values as free-form text (main background, secondary background, accent, text, details). Catalog + hex values: `design-system.md §2`.
- Steel is the recommended default; the named-palette values are canonical — do not improvise them. If no answer: default palette (values already known).
- From the 5 light roles, Claude **derives** and announces: supporting light tokens (`bg-muted`, `bg-elevated`, `text-subtle`, `text-muted`, `border-subtle`, `border-strong`), the 5 accent stops (`primary-50/400/700/800/900`), `onPrimary`, and the **whole dark theme** (lightness targets in `design-system.md §2`).
- Written to `styles_light.qss` + `styles_dark.qss` (neutrals) and `config.py` (`PRIMARY_*`, `ON_PRIMARY`, `ICON_COLORS`). Semantic colors stay fixed.
- **Contrast check (WCAG AA, non-blocking)**: compute text/bg, text-subtle/bg, accent/bg, onPrimary/accent; if a ratio fails AA, report it (`color — ratio — target`) and ask the user to confirm or adjust before continuing.
- The global `design-system.md` stays unchanged.

Then announce the **provisional** calibration:

Provisional calibration: [Small | Medium/Large] — [N] batches (incl. 1 test batch if enabled)
(Confirmed at the end of Phase 2, after counting the real features.)

Apply the CALIBRATION table in `CLAUDE.md` (canonical source).

## Write the spec

Write `docs/specs/01-scoping.md` (in the user's language) capturing: objective, DB, preferences, i18n, tests, packaging, the **palette** (name or custom; the 5 light roles + the derived dark theme + accent stops + onPrimary; semantic kept fixed) and the contrast-check result, validated libraries, and the provisional calibration. If `docs/specs/` does not exist yet, create it (it will live in the generated project root).

Chain immediately to Phase 2 (`/python-p2-featuring`).
