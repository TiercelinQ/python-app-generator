---
name: python-migrate-design
description: Convert a Python/PySide6 app generated with design system v1.x to v2.0 — QSS tokens (accent-tinted neutrals, derived semantics), icons (qtawesome → vendored Lucide SVGs), hover model, radius, sliding underline — without changing any behavior. Proposed by /python-load-project when a legacy app is detected; runs only on explicit validation.
model: sonnet
---

# /python-migrate-design — Convert a v1.x app to design system v2.0

## Role
Migration engineer — re-skin a delivered app to the v2.0 design system with zero behavior change.

## Goal
The app renders under the full v2.0 visual language (tokens, icons, states, motion) while every feature, signal, and business rule behaves exactly as before.

## Deliverable
The converted files on disk (QSS sheets, `config.py` colors, icon usages, new helpers) + refreshed app `README.md` / `CLAUDE.md` / `docs/specs/04-architect.md` token table + passing verification + a conversion summary.

---

## Prerequisite

The project is loaded (`/python-load-project`) and detected on design system **v1.x** (README reference; markers: `qtawesome` in `requirements.txt`/imports, no `resources/icons/`, no `utils/icons.py`). If the app is already on v2.0, say so and stop.

**Load context**: `design-system.md` (v2.0) + `layout.md` (v4.1) + `@rules/qss.md` + `@rules/config.md` + `@rules/verification.md`, and the app's `docs/specs/01-scoping.md` (original palette choice) + `docs/specs/04-architect.md` (locked contract).

## Step 1 — Inventory (read-only)

- `resources/styles_light.qss` / `styles_dark.qss`: current neutrals/semantics, identify the accent (`config.PRIMARY_600`).
- `docs/specs/01-scoping.md`: was the palette a **named preset** (Steel Blue, Teal…) or **custom** (5 explicit roles)?
- `config.py`: `PRIMARY_*`, `ICON_COLORS`, `SPLASH_COLORS` (if splash).
- Views/controllers (`Grep` for `qtawesome`, `qta.icon`, `fa6s.`): every icon usage, per file.
- The retained composition (`docs/specs/03-surfaces.md`): does it have tabs / horizontal navigation, and where does the selected-tab QSS border-bottom live?

## Step 2 — Palette conversion decision

- **Preset palette** → re-derive **everything** from the accent per `design-system.md §2`: accent stops, accent-tinted neutrals (both themes), per-project semantic colors (info = accent). Full v2.0 atmosphere.
- **Custom palette** → the roles the user explicitly chose in Phase 1 (recorded in `01-scoping.md`) become **v2.0 overrides** (they win over the tinted targets); everything else derives from the accent.
- Announce the derived token set and run the **AA contrast check** (same pairs as `/python-p1-scoping` §2), reporting failures without blocking.

## Step 3 — Conversion plan (validation gate)

Present the plan (in the user's language): files touched, the icon mapping table (below) instantiated with the icons actually found, the palette decision, and the note that **no behavior changes** (no model, controller signal, or i18n edit). **→ Validation required before writing.**

## Step 4 — Conversion (single batch, complete files)

1. **QSS sheets** — full v2.0 rewrite of both sheets per `@rules/qss.md`: tinted neutrals + derived semantics as literal hex, `border-radius: 5px` (3px nested), neutral hover = border strengthening (transparent 1px borders added so layout never shifts), `pressed` = `bg-muted`, drawer/dialog borders promoted to `border-strong`, statusbar `text-subtle` derived value, no pinned `font-family`, selected-tab border-bottom removed (the underline widget replaces it), `/* token : … */` comments updated.
2. **`config.py`** — derived `PRIMARY_*`/`ON_PRIMARY` (unchanged if the accent is kept), `ICON_COLORS` rewritten with the derived values, add `ICON_SM/MD/LG`, `ICON_STROKE = 1.75`, `ANIM_DEFAULT_MS = 160`, `ANIM_SLOW_MS = 240`, `ANIMATIONS_ENABLED = True`; `SPLASH_COLORS` re-derived if the splash is on.
3. **Icons** — remove `qtawesome` from `requirements.txt`; add `utils/icons.py` (Lucide SVG → themed `QIcon` helper, `design-system.md §10`); vendor the needed SVGs into `resources/icons/` (source: npm `lucide-static` or the official Lucide repo — verify each name at the source); replace every `qta.icon("fa6s.…", color=…)` call with `get_icon("…", color_key, theme, size)` using the mapping below.
4. **Underline** — only if the retained composition has tabs / horizontal navigation (the underline exists nowhere else, `design-system.md §8`): add `views/sliding_underline.py` (reference implementation in §8) wired to the tab bar on tab change (animated) and on resize/mount (snap). Snaps when `config.ANIMATIONS_ENABLED` is off.
5. **Docs** — app `README.md`: design system reference → `v2.0` (+ layout `v4.1`), stack line Icons → Lucide, `qtawesome` removed from prerequisites; app `CLAUDE.md`: dated migration note under `## Deviations from the framework` (or a `## Design system migration` block); `docs/specs/04-architect.md`: refresh the tokens → QSS table values, add the new files (`utils/icons.py`, `views/sliding_underline.py`, `resources/icons/`), append a dated migration note (this validated run is the contract amendment).
6. **Changelog** — append a `### Changed` entry under `## [Unreleased]` in `docs/release/CHANGELOG.md` (`@rules/versioning.md`): `- Migrated UI to design system v2.0.` (English, no version bump; migrate-design infers MINOR at `/python-release`). If the file is absent (legacy app never initialized), skip silently and suggest `/python-load-project`.

### Icon mapping — Font Awesome 6 (`fa6s.*`) → Lucide SVG name

| FA 6 name | Lucide SVG | FA 6 name | Lucide SVG |
| --------- | ---------- | --------- | ---------- |
| `house` | `house` | `magnifying-glass` | `search` |
| `gear` | `settings` | `plus` | `plus` |
| `circle-check` | `circle-check` | `trash` / `trash-can` | `trash-2` |
| `triangle-exclamation` | `triangle-alert` | `pen` / `pencil` | `pencil` |
| `circle-xmark` | `circle-x` | `floppy-disk` | `save` |
| `circle-info` | `info` | `xmark` | `x` |
| `sun` / `moon` | `sun` / `moon` | `bars` | `menu` |
| `chevron-right` / `chevron-down` | `chevron-right` / `chevron-down` | `user` | `user` |
| `arrows-rotate` / `rotate` | `refresh-cw` | `download` / `upload` | `download` / `upload` |
| `check` | `check` | `spinner` | `loader-circle` |
| `arrow-right-from-bracket` | `log-out` | — | — |

Any icon not in this table: pick the closest Lucide equivalent, verify the SVG exists at the vendoring source before copying, and list the chosen mapping in the conversion summary. Never invent a name.

## Step 5 — Verification and summary

- Run `@rules/verification.md §A` in full (`pip install` → `ruff check` → `ruff format --check` → `mypy` → `pytest` if tests exist → `python main.py` smoke) — a failure is blocking.
- Residual grep: `qtawesome`, `fa6`, `qta.icon` must return nothing in the source; the old v1.x hex must be gone from the sheets and `config.py` (neutrals `#1C1C1C`, `#F9FAFB`, `#F3F4F6`, `#9CA3AF`, `#E5E7EB`, `#D1D5DB`, `#6B7280` and semantics `#16A34A`, `#D97706`, `#DC2626`, `#2563EB` — `#FFFFFF` legitimately survives as `ON_PRIMARY`).
- Manual visual pass by the user: state that colors, radius, hover, and the tab underline are the only intended visible changes — every feature must behave identically. Report the conversion summary (files, icon mappings, AA results).
- After an anomaly: cleanup protocol (`@rules/mvc.md`), then offer `/python-save-memory`.

## Anti-patterns — what NOT to do

- **Do not** run without the Step 3 validation, and do not convert partially — the app is either fully v1.x or fully v2.0 (never a mix).
- **Do not** touch models, controllers, signals, i18n strings, or any business logic — this is a re-skin.
- **Do not** redesign the layout/composition — the retained Phase 3 composition stays; only its skin changes.
- **Do not** improvise a Lucide name — map it, verify the SVG exists, report it.
- **Do not** leave qtawesome residue (dependency, imports, `fa6s.` names, old fixed hex in `ICON_COLORS`).
- **Do not** convert the palette of a custom-palette app without preserving its explicitly chosen roles as overrides (Step 2).

## Integrity verification

Detailed in `@rules/verification.md`. Key points: §A executable suite green after conversion; zero `qtawesome`/`fa6` residue in source and `requirements.txt`; both QSS sheets fully v2.0 (tinted neutrals, derived semantics, radius token, border-strengthening hover, no selected border-bottom) with `utils/icons.py` + `resources/icons/` + `views/sliding_underline.py` present; app README/CLAUDE.md/04-architect.md updated with the v2.0 reference and the dated migration note.
