# QSS and styles rules — v2.0

> Binding QSS reference for Python/PySide6 apps. Built on `design-system.md v2.0` + `layout.md v4.1` (versions tracked per file — `design-system.md §1`).

## Changelog

| Version | Date       | Main change                                                                    |
| ------- | ---------- | ------------------------------------------------------------------------------ |
| 2.0     | 2026-07-16 | design-system v2.0 alignment: radius 5px · accent-tinted neutrals + derived semantics (default hex refreshed) · hover = border strengthening (no `bg-muted` fill) · tabs indicator = `SlidingUnderline` widget (QSS drops the selected border-bottom) · floating layers `border-strong` · no pinned `font-family` · Lucide icon helper note (qtawesome retired) |
| 1.1     | 2026-07-14 | Pattern-aware anchors note + layout.md v4.0 reference                           |
| 1.0     | 2026-07-11 | Initial versioned QSS ruleset: tokens, light/dark sheets, flat design, `Fusion` requirement, statusbar `text-subtle`. |

## Principles

- Zero hardcoded visual value in Python. Everything in `styles_light.qss` / `styles_dark.qss` or `config.py`.
- Every styled widget has an `objectName` matching a named QSS rule.
- Every QSS rule carries a `/* token : [name] */` comment tracing to `design-system.md`.
- Dark mode: complete sheet replacement (`styles_light.qss` → `styles_dark.qss`). Never a partial override.
- **Two mandatory files**: `resources/styles_light.qss` + `resources/styles_dark.qss`. No single conditional file.
- **Fusion style mandatory** in `main.py`: `app.setStyle("Fusion")` right after `QApplication(sys.argv)`. The native Windows style (`windowsvista`) paints native frames for tabs/widgets and partially ignores QSS borders — QSS only becomes authoritative under Fusion. Without it, stroke-based styling (e.g. `QTabBar` borders) renders wrong on Windows.
- **No `font-family` in the sheets** (`design-system.md §1`): the `QApplication` default font is the native OS face. QSS sets sizes and weights only.
- **QSS cannot transition**: hover/focus state changes apply instantly (accepted, `design-system.md §6`). The only animated visuals are the drawer slide and the `SlidingUnderline` widget, both `QPropertyAnimation` driven.

## Mandatory internal organization

```qss
/* ============================================================
   styles_[light|dark].qss — [APP_NAME] v[VERSION]
   Theme: [light | dark]
   Reference: design-system.md v2.0 (project palette)
   ============================================================ */

/* --- BASE -------------------------------------------------- */
/* token : bg / text */
QMainWindow { background-color: #FDFEFF; color: #0F181E; }

/* --- TOPBAR ------------------------------------------------ */
/* sections mirror the retained composition (layout.md §12) */
/* token : bg / border / topbar-height */
QWidget#topbar { background-color: #FDFEFF; border-bottom: 1px solid #E1E6EA;
                 min-height: 48px; max-height: 48px; padding: 0 16px; }

/* --- TABS -------------------------------------------------- */
/* token : text-subtle / primary / border / topbar-height */
/* Style the QTabBar WIDGET, not only ::tab — otherwise the native engine paints
   its own background block behind the tabs (grey/blue, not matching the topbar). */
QTabBar#nav_tabs { background-color: transparent; border: none; }
/* v2.0: the selected indicator is the SlidingUnderline widget (design-system §8),
   NOT a QSS border-bottom. outline:none removes the native focus rectangle.
   The transparent 1px border is the hover reservation (border strengthening). */
QTabBar::tab { background-color: transparent; color: #65717B;
               border: 1px solid transparent; border-radius: 5px; outline: none; }
QTabBar::tab:selected { color: #4682B4; }                        /* primary (light) */
QTabBar::tab:hover:!selected { border: 1px solid #E1E6EA; }      /* border strengthening */

/* --- MAIN CONTENT ------------------------------------------ */
/* token : bg / spacing-6 */
QWidget#main_content { background-color: #FDFEFF; padding: 24px; }

/* --- TOAST ------------------------------------------------- */
/* token : *-50 / *-600 / border-width-accent / radius */
QWidget#toast_success { background-color: #EFF6F3; border-left: 4px solid #328F6D; border-radius: 5px; }
QWidget#toast_warning { background-color: #F8F5EC; border-left: 4px solid #A58327; border-radius: 5px; }
QWidget#toast_danger  { background-color: #F8EFF1; border-left: 4px solid #BA3B52; border-radius: 5px; }
QWidget#toast_info    { background-color: #EDF3F8; border-left: 4px solid #4682B4; border-radius: 5px; }   /* info = accent */

/* --- BUTTONS ----------------------------------------------- */
/* token : primary-600/700/800 / onPrimary / border / border-strong / text / text-subtle
           danger-600/700/800 / bg-muted / radius */
QPushButton { border-radius: 5px; }
QPushButton#btn_primary           { background-color: #4682B4; color: #FFFFFF; border: none; }
QPushButton#btn_primary:hover     { background-color: #396A93; }   /* primary-700 */
QPushButton#btn_primary:pressed   { background-color: #2F5879; }   /* primary-800 */
QPushButton#btn_secondary         { background-color: transparent; color: #0F181E; border: 1px solid #E1E6EA; }
QPushButton#btn_secondary:hover   { border: 1px solid #96A4B0; }   /* border-strong — stroke hover */
QPushButton#btn_secondary:pressed { background-color: #EEF1F4; }   /* bg-muted — press feedback */
QPushButton#btn_danger            { background-color: #BA3B52; color: #FFFFFF; border: none; }
QPushButton#btn_danger:hover      { background-color: #A23448; }   /* danger-700 */
QPushButton#btn_danger:pressed    { background-color: #8A2C3D; }   /* danger-800 */
QPushButton#btn_ghost             { background-color: transparent; color: #65717B; border: 1px solid transparent; }
QPushButton#btn_ghost:hover       { border: 1px solid #E1E6EA; color: #0F181E; }   /* border + text */
QPushButton#btn_ghost:pressed     { background-color: #EEF1F4; }   /* bg-muted */
QPushButton:disabled              { color: rgba(15, 24, 30, 0.4); }   /* opacity-disabled 40% */

/* --- INPUT FIELDS ------------------------------------------ */
/* token : border / text / primary-600 / spacing-2 / spacing-3 / radius */
/* Focus: 2px border without layout shift — compensate padding by 1px on :focus */
QLineEdit { border: 1px solid #E1E6EA; border-radius: 5px; color: #0F181E; padding: 8px 12px; }
QLineEdit:focus { border: 2px solid #4682B4; padding: 7px 11px; }
/* combobox-popup: 0 is load-bearing under Fusion: applying ANY QSS to a QComboBox
   flips its popup to the Fusion "menu" mode, which crops item height and shows
   parasitic scroll arrows even for 2 items. `combobox-popup: 0` restores the plain
   list popup (sized to content, scrolls past maxVisibleItems). Also style ::item
   (colour + min-height) or the popup items render illegible under Fusion. */
QComboBox { border: 1px solid #E1E6EA; border-radius: 5px; color: #0F181E; padding: 8px 12px;
            combobox-popup: 0; }
QComboBox:focus { border: 2px solid #4682B4; padding: 7px 11px; }
QComboBox QAbstractItemView { background-color: #FDFEFF; color: #0F181E;
                              border: 1px solid #E1E6EA; outline: 0; }
QComboBox QAbstractItemView::item { color: #0F181E; padding: 6px 10px; min-height: 24px; }

/* --- TABLES ------------------------------------------------ */
/* token : bg-subtle / text-subtle / border-strong / border-subtle / border / primary-bg / primary */
QTableView { border: none; gridline-color: #ECF0F3; }
QHeaderView::section { background-color: #F5F8FA; border-bottom: 2px solid #96A4B0; }
QTableView::item:selected { background-color: #EDF3F8; color: #4682B4; }   /* primary-bg / primary (design-system §8) */
QTableView::item:hover { background-color: #F5F8FA; }   /* bg-subtle — wide-row secondary cue (§8); the row border strengthening is carried by the delegate/row style where available */

/* --- STATUSBAR --------------------------------------------- */
/* token : bg-muted / border / text-subtle / statusbar-height / xs */
/* Statusbar text = text-subtle (NOT text-muted) — design-system.md §12 (WCAG), layout.md §7. */
QStatusBar { background-color: #EEF1F4; border-top: 1px solid #E1E6EA;
             min-height: 28px; max-height: 28px; padding: 0 16px;
             font-size: 12px; color: #65717B; }

/* --- DRAWER ------------------------------------------------ */
/* token : bg-elevated / border-strong / spacing-6 — floating layer (design-system §5) */
QWidget#drawer { background-color: #FDFEFF; border-left: 1px solid #96A4B0; padding: 24px; }

/* --- DIALOG / MODAL ---------------------------------------- */
/* token : bg / border-strong / radius / spacing-6 — floating layer (design-system §5) */
QDialog { background-color: #FDFEFF; border: 1px solid #96A4B0; border-radius: 5px; min-width: 480px; }

/* --- SCROLLBARS -------------------------------------------- */
/* token : bg-muted / border-strong / radius */
QScrollBar:vertical   { background: transparent; width: 12px; margin: 0; }
QScrollBar:horizontal { background: transparent; height: 12px; margin: 0; }
QScrollBar::handle:vertical,
QScrollBar::handle:horizontal        { background: #EEF1F4; border-radius: 5px; min-height: 24px; min-width: 24px; }
QScrollBar::handle:hover             { background: #96A4B0; }   /* border-strong */
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }   /* no arrows */
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

/* --- TOOLTIP ----------------------------------------------- */
/* token : text (inverted bg) / bg / border / radius / spacing-2 / xs */
QToolTip { background-color: #0F181E; color: #FDFEFF; border: 1px solid #E1E6EA;
           border-radius: 5px; padding: 4px 8px; font-size: 12px; }

/* --- SELECTION (text) -------------------------------------- */
/* token : primary-bg / text */
QLineEdit, QTextEdit, QPlainTextEdit {
    selection-background-color: #EDF3F8;   /* selection-bg light (primary-50) */
    selection-color: #0F181E;              /* selection-text light */
}
```

> Dark sheet equivalents (Steel Blue default, derived): scrollbar handle `#293138` (bg-muted), hover `#52626F` (border-strong); tooltip bg `#293138`, color `#F2F5F7`, border `#52626F`; selection bg `#2A4F72` (primary-900), color `#F2F5F7`; `QTableView::item:selected` bg `#2A4F72` + text `#5A9FD4` (primary-400); tab selected color `#5A9FD4`; hover borders `#323B43` (border) / `#52626F` (border-strong); disabled `rgba(242, 245, 247, 0.4)`.
>
> Dark toast backgrounds (`*-50` dark role tint, `bg` 82 % + `*-600` dark 18 %): `toast_success` `#26372F`, `toast_warning` `#392F1B`, `toast_danger` `#38222B`, `toast_info` `#2A4F72` (primary-900); left borders use the `*-600` dark accents (`#6EC4A4` / `#D2B460` / `#CB7282` / `#5A9FD4`). Toast message text uses `text` (`#F2F5F7` dark).
>
> Dark buttons: `btn_primary` keeps the accent `#4682B4` (primary-600, chromatic in both themes) with **white text**, hover `#396A93` / pressed `#2F5879`. The danger **fill** stays the light `danger-600` `#BA3B52` in both themes with white text (design-system §9), hover `#A23448` / pressed `#8A2C3D` (danger-700/800, mode-agnostic); the dark `#CB7282` is the **foreground** danger (toast border/icon), not the button fill. The accent stops are a single chromatic ramp shared by both sheets; `config.py PRIMARY_*` holds them. The dark foreground accent (active text/border/icon/focus) uses the brighter `primary-400 #5A9FD4`.

## Reference tokens (design-system.md v2.0 — default Steel Blue palette, derived)

### Light mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #FDFEFF |
| `bg-subtle`     | #F5F8FA |
| `bg-muted`      | #EEF1F4 |
| `bg-elevated`   | #FDFEFF |
| `text`          | #0F181E |
| `text-subtle`   | #65717B |
| `text-muted`    | #98A4AE |
| `border`        | #E1E6EA |
| `border-subtle` | #ECF0F3 |
| `border-strong` | #96A4B0 |
| `primary-50`    | #EDF3F8 |
| `primary-600`   | #4682B4 |
| `primary-700`   | #396A93 |
| `primary-800`   | #2F5879 |

### Dark mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #181C20 |
| `bg-subtle`     | #20272C |
| `bg-elevated`   | #252C32 |
| `bg-muted`      | #293138 |
| `text`          | #F2F5F7 |
| `text-subtle`   | #94A2AD |
| `text-muted`    | #5F6C77 |
| `border`        | #323B43 |
| `border-subtle` | #272F35 |
| `border-strong` | #52626F |
| `primary-400`   | #5A9FD4 |
| `primary-600`   | #4682B4 |
| `primary-700`   | #396A93 |
| `primary-800`   | #2F5879 |
| `primary-900`   | #2A4F72 |
| `onPrimary`     | #FFFFFF |

Semantic values (both themes): `design-system.md §2` (derived per project; the defaults above pair with `success-600` #328F6D/#6EC4A4, `warning-600` #A58327/#D2B460, `danger-600` #BA3B52/#CB7282, info = accent).

### Depth by stroke (non-negotiable)

- `border-radius: 5px` on every rounded element (buttons, fields, toasts, modals, scrollbar handles); nested elements (menu items inside a 5px container) use 3px. Never another radius value.
- No shadow (`box-shadow`, `QGraphicsDropShadowEffect`). No gradient.
- Floating layers (drawer, dialog, dropdown, toast) mark their elevation with `border-strong` — never a shadow.

### Focus indicator

- `outline-offset` is not reliable in QSS. Show focus with a 2px border in the focus color, compensating padding so the layout does not shift (see the input-field example: 1px/8-12px default → 2px/7-11px on `:focus`).
- Light: `primary-600`. Dark: `primary-400`. Never remove the focus indicator.

### Hover — border strengthening

- Neutral interactive elements hover by **stroke**, not fill (`design-system.md §8`): default state carries a transparent 1px border (or its real `border`); on hover the border climbs one step (transparent → `border`; `border` → `border-strong`). Instant (QSS cannot transition) — accepted.
- `pressed` keeps the `bg-muted` fill (transient feedback). Wide list/table rows may add `bg-subtle` as a secondary hover cue.

### Tabs indicator — SlidingUnderline

The selected tab is marked by the `SlidingUnderline` widget (`views/sliding_underline.py`, `design-system.md §8`), **not** by a QSS `border-bottom`. QSS gives the tab row its base styling only; the widget slides on tab change (240ms `OutCubic`, snaps when `config.ANIMATIONS_ENABLED` is off). Keep `setDrawBase(False)` on the `QTabBar`.

## Per-project palette

In Phase 1 the project picks a **palette** (named or custom): the accent is mandatory (→ `primary-600`), the four other roles are optional overrides (fond principal → `bg`, fond secondaire → `bg-subtle`, texte → `text`, détails → `border`). Claude derives everything else (`design-system.md §2`): the accent stops, `onPrimary`, the **accent-tinted neutrals** for both themes, and the **per-project semantic colors** (hue anchors harmonized ±6° toward the accent; info = accent), then writes the resolved hex into **both** `styles_light.qss` and `styles_dark.qss` (+ accent stops and `ICON_COLORS`/`ON_PRIMARY`, and `SPLASH_COLORS` if the splash is on, in `config.py`). An explicit override wins over the tinted target for its token; its supporting tokens derive from it. The values above are the **default palette** — a custom palette replaces them throughout both sheets. The global `design-system.md` stays unchanged (it documents the rule, not the per-project values).

## Anti-patterns — what NOT to do

- **Do not** set a color/size/font directly in Python (`setStyleSheet("...")` inline, `QColor(...)` for a themed value). Route it through the QSS sheets + an `objectName`. Documented exceptions: `config.PRIMARY_*`/`ICON_COLORS`/`SPLASH_COLORS`, and the `SlidingUnderline` widget reading `config.PRIMARY_*` (`design-system.md §11`).
- **Do not** write a QSS value without a `/* token : ... */` comment tracing to `design-system.md`.
- **Do not** handle dark mode with a `[theme]`-conditional single sheet or partial override — replace the whole sheet.
- **Do not** use a radius other than 5px (or 3px nested), and never add `box-shadow`, `QGraphicsDropShadowEffect`, or a gradient — depth is stroke-based.
- **Do not** style a widget without giving it an `objectName` (or use a generic class selector when a named rule is expected).
- **Do not** style a `QTabBar` only via `::tab` — also set the `QTabBar` widget background to `transparent`, add `outline: none` on `::tab`, and `setDrawBase(False)` on the widget. The selected indicator is the `SlidingUnderline` widget, never a QSS `border-bottom`. **Root cause of persistent left/right/top borders on Windows: the native `windowsvista` style** — none of the QSS above works until `app.setStyle("Fusion")` is set in `main.py`. Verify in both themes on a real Windows machine (the offscreen platform does not use `windowsvista`).
- **Do not** hover by `bg-muted` fill on a neutral element — hover is border strengthening (§8); `bg-muted` is the `pressed` feedback.
- **Do not** put icon colors in QSS — Lucide icon colors live in `config.py` (`ICON_COLORS`), consumed by `utils/icons.py` (documented exception).
- **Do not** put splash colors in QSS — a `QSplashScreen` is painted programmatically, so its `bg`/`text` live in `config.py` (`SPLASH_COLORS`), the second documented exception (only when the splash screen is on, Phase 3). See `@rules/splash.md`.
- **Do not** pin a `font-family` in the sheets — the QApplication system font is the face (`design-system.md §1`).

## Integrity verification

Detailed in `@rules/verification.md`. Key points: zero hardcoded visual value in Python (no inline `setStyleSheet`, no themed `QColor`) — the documented exceptions are `PRIMARY_*`/`ICON_COLORS`, `SPLASH_COLORS` if the splash is on, and the `SlidingUnderline` widget; both sheets `resources/styles_light.qss` + `resources/styles_dark.qss` present, dark mode = full sheet replacement (no partial override); every styled widget carries an `objectName` matching a named rule, and every QSS rule carries its `/* token : … */` comment; `app.setStyle("Fusion")` set in `main.py` right after `QApplication(sys.argv)`; stroke-based depth held (radius 5px/3px only, no shadow, no gradient, hover by border strengthening, floating layers on `border-strong`); statusbar text = `text-subtle`; tabs indicator = `SlidingUnderline`, no QSS selected border-bottom.
