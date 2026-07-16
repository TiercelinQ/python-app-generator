---
name: python-p4-architect
description: Phase 4 of the Python app generation cycle — complete architectural contract (tree, role of each file, tokens → QSS table, source→test mapping), written to the contract spec and locked after validation.
model: sonnet
---

# /python-p4-architect — Architectural contract

## Role
Software architect — design the locked structure the whole build will follow.

## Goal
Produce a complete, unambiguous architectural contract that freezes the file tree, QSS mapping, and (if tests) the source→test mapping.

## Deliverable
`docs/specs/04-architect.md` (written in the user's language) — the locked source of truth + on-screen contract.

---

**Phase banner (show first)** — before anything else, output the phase banner as plain Markdown in the user's language, **never inside a code block or fenced block**. Three blocks, each on its own line: (1) H2 heading: Phase 4/5 — Architecture; (2) progress line: Scoping ✓ · Features ✓ · Surfaces ✓ · ▶ Architecture · Development; (3) intent in italics: Lock the file/structure contract. See `## PIPELINE` in `CLAUDE.md`.

At start: read `design-system.md`, `layout.md` (no longer auto-imported), `@rules/mvc.md` (tree, batches, MVC conventions) and `@rules/qss.md` (tokens → QSS). **If the Salesforce CLI integration is on (Phase 1), also read @rules/sf-cli.md** (runner, exceptions, Org Manager scaffold). Read `docs/specs/01-scoping.md` through `03-surfaces.md` for the validated decisions.

Present (in the user's language, as plain Markdown — never inside a code block):

1. **Complete project tree** (model: `@rules/mvc.md`) with the role of each file.

   **If the Salesforce CLI integration is on (Phase 1)**: add the runner + Org Manager files to the tree (`models/sf_cli.py`, `views/org_manager_view.py`, `controllers/org_manager_controller.py`). The `sf` runtime prerequisite and the `SF_CLI_PATH` setting are part of the contract. See @rules/sf-cli.md.

2. **Tokens → planned QSS rules table** (`styles_light.qss` + `styles_dark.qss` selectors and the tokens they consume):

| design-system.md token | Light value | Dark value | Target QSS rule |
| ---------------------- | ----------- | ---------- | --------------- |
| `bg`                   | #FDFEFF     | #181C20    | QMainWindow, #main_content, #topbar |
| `primary-600`          | #4682B4     | #4682B4    | #btn_primary; QTabBar::tab:selected color + SlidingUnderline (light) |
| …                      | …           | …          | …               |

   The example rows use the **default composition** (topbar + tabs). The `objectName` anchors and QSS targets always follow **the retained composition from `docs/specs/03-surfaces.md`** — another pattern (`layout.md` §12) replaces them with its own widgets and anchors (`#sidebar`, `#menu_bar`, `#master_list`/`#detail_pane`).

   **If the splash screen is on (Phase 3)**: add `views/splash_screen.py` to the tree, note the `SPLASH_MIN_DURATION_MS` + `SPLASH_COLORS` constants in `config.py`, and the `main.py` orchestration (`create_splash` before `MainWindow`, `splash.finish(window)` after the min duration). The icon source (Phase 1 icon reused, path provided in Phase 3, or text-only) is part of the contract. See @rules/splash.md.

3. **Source → test mapping** (only if tests enabled in Phase 1 Q5): each source module → its `test_*.py` file (incl. `models/sf_cli.py` / `controllers/org_manager_controller.py` if the Salesforce integration is on). See `@rules/tests.md`.

**→ Validation required. This contract is locked.**

Any deviation (merge, split, rename, addition, removal of a file or library) requires:

1. Stop.
2. Declare the deviation + justification.
3. Validation before resuming.

**Blocking rule**: do not deliver Batch 1 until validation is explicit.

## Write the spec

Once validated, write the full contract to `docs/specs/04-architect.md` (in the user's language). This file is the **locked source of truth** re-read by `/python-p5-development`, `/python-load-project`, `/python-show-contract`, `/python-add-feature`, and `/python-refactor-code`.

→ Chain to `/python-p5-development` after validation.
