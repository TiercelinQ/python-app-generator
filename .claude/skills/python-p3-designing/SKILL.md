---
name: python-p3-designing
description: Phase 3 of the development cycle — layout proposal from layout.md, grouped customization questions, validated synthesis written to the layout spec before Phase 4.
model: sonnet
---

# /python-p3-designing — Layout proposal

## Role
UI designer — map the validated features onto the binding layout system.

## Goal
Define the concrete layout (tabs, drawer/modal, toast position) within `layout.md` constraints.

## Deliverable
`docs/specs/03-designing.md` (written in the user's language) + on-screen synthesis.

---

## Instructions — Phase 3: Layout proposal

**Phase banner (show first)** — before anything else, output the phase banner as plain Markdown in the user's language, **never inside a code block or fenced block**. Three blocks, each on its own line: (1) H2 heading: Phase 3/5 — Design; (2) progress line: Scoping ✓ · Features ✓ · ▶ Design · Architecture · Development; (3) intent in italics: Map the validated features onto the layout. See `## PIPELINE` in `CLAUDE.md`.

**Read `design-system.md` and `layout.md` first** (no longer auto-imported).

Based on the features validated in Phase 2 (`docs/specs/02-featuring.md`), propose a layout drawn from `layout.md`, then ask the closed customization questions with `AskUserQuestion` (clickable options, recommended first; ≤ 4 options each, **Other** for the rest; split into ≤ 4-question calls).

### Step 1 — Initial proposal

Produce (in the user's language):

## Proposed layout — [NOM_APP]

**Structure**
[Description: topbar, tabs, main content, statusbar]

**Tabs**
| Tab | Content |
| ------ | ------- |
| …      | …       |

**Recurring components**
- [Table / Form / Tree / Charts — depending on the features]

> If the Salesforce CLI integration is on (Phase 1), present the **Org Manager** surface as a baseline: a tree/list of orgs (connected/disconnected state via `ICON_COLORS`, default org marked) with add / remove / reconnect / set-default / refresh actions, typically its own tab. Confirm its placement. See @rules/sf-cli.md.

### Step 2 — Customization questions (`AskUserQuestion`)

For each question, mark the option you recommend with `(recommended)`, chosen from the validated feature context.

A few choices to confirm:

1. Tab position in the topbar:
   A. After the logo and name (left-aligned)
   B. Centered

2. Secondary panel: drawer or modal?
   A. Drawer (persistent side panel)
   B. Modal (overlay window)
   C. None

[If A — Drawer:]
3. Drawer width:
   A. Fixed 320px (design-system.md default)
   B. Fixed custom — specify the value
   C. Dynamic (adapts to content)

[If B — Modal:]
3. Modal size:
   A. Fixed — specify width × height
   B. Dynamic (adapts to content)

4. Modal internal layout:
   A. Header + main content + footer
   B. Header + 2 columns (main content) + footer
   C. Header + main content (no footer)
   D. Other — I'm not sure, help me choose

5. Toast position:
   A. Top-right (default)
   B. Top-left
   C. Top-center
   D. Bottom-right
   E. Bottom-left
   F. Bottom-center

Show only the relevant questions for the feature context. If the project clearly needs no drawer or modal, skip questions 3/4 and note the absence of a secondary panel. Question 5 (toasts) is always asked.

If the user picks D on question 4: ask 3 questions with `AskUserQuestion` to help define the layout:

To help you choose the layout:

a. What is the main purpose of this modal?
b. Are there actions to perform from this modal? Yes / No
c. Is the content homogeneous (single block) or heterogeneous (several sections)?

Based on the answers, propose 2 suited layouts with a justified recommendation, then confirm before the synthesis.

6. **Splash screen** (`AskUserQuestion`): `Yes` (recommended) · `No`. A `QSplashScreen` shown at launch until the main window is ready, following the design system (flat, palette, dark mode). See @rules/splash.md.
   - **If `Yes`**: Python has no standalone application icon in Phase 1. Ask, as free-form text, for an **optional** icon path (`.ico`/`.png`) to show on the splash — "Icon to display on the splash? (path, or leave empty for text-only)". A provided image is saved as `resources/icon.ico`; empty → text-only splash (app name). If `.exe` packaging is on, the splash reuses the packaging `resources/icon.ico` (offer to reuse it or provide another).

### Step 3 — Final synthesis

Produce the complete synthesis (in the user's language): topbar, tabs, secondary panel, recurring components, toast position, splash screen on/off + icon source, applied constraints.

→ Validation required before Phase 4.
  Confirm or list the adjustments.

**Blocking rule**: do not move to Phase 4 until validation is explicit.

## Write the spec

Once validated, write the synthesis to `docs/specs/03-designing.md` (in the user's language).

Chain to `/python-p4-architect` after validation.
