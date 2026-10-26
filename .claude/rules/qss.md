# QSS and styles rules - v2.1

> Binding QSS reference for Python/PySide6 apps. Built on `design-system.md v2.1` + `layout.md v4.2` (versions tracked per file - `design-system.md §1`).

## Changelog

| Version | Date       | Main change |
| ------- | ---------- | ----------- |
| 2.1     | 2026-10-26 | design-system v2.1 alignment: surface ladder N0-N3 (`bg-panel`) with recomputed neutrals · AA-darkened `primary-600` (`#3D729E`) · `danger-fill` · control edge and neutral hover on `border-strong` · selection bar painted by `SelectionBarDelegate` · focus ring inside the widget, `text` on filled buttons, keyboard-only through `Qt.TabFocus` · rules selected by dynamic property (`variant`, `btnSize`, `role`, `tone`, `error`, `selected`, `active`) with `repolish` · pre-blended `disabled-*` and `overlay` rgba literals (QSS has no opacity) · `QPalette` and color scheme set with the sheet by `apply_theme` · `{{icon:NAME:KEY}}` placeholder for images referenced from QSS · `FittedList` for item views that host widgets · tooltip on `bg-elevated` |
| 2.0     | 2026-07-16 | design-system v2.0 alignment: radius 5px · accent-tinted neutrals + derived semantics (default hex refreshed) · hover = border strengthening (no `bg-muted` fill) · tabs indicator = `SlidingUnderline` widget (QSS drops the selected border-bottom) · floating layers `border-strong` · no pinned `font-family` · Lucide icon helper note (qtawesome retired) |
| 1.1     | 2026-07-14 | Pattern-aware anchors note + layout.md v4.0 reference |
| 1.0     | 2026-07-11 | Initial versioned QSS ruleset: tokens, light/dark sheets, flat design, `Fusion` requirement, statusbar `text-subtle`. |

## Principles

- Zero hardcoded visual value in Python. Everything in `styles_light.qss` / `styles_dark.qss` or `config.py`.
- Every styled widget has an `objectName` or a dynamic property matching a named QSS rule.
- Every QSS rule carries a `/* token : [name] */` comment tracing to `design-system.md`.
- Dark mode: complete sheet replacement (`styles_light.qss` -> `styles_dark.qss`) through `apply_theme` (`utils/styles.py`). Never a partial override.
- **Two mandatory files**: `resources/styles_light.qss` + `resources/styles_dark.qss`. No single conditional file. A project may keep one template with `{{token}}` placeholders and generate the two sheets; the generated sheets are what the app loads and what review reads.
- **Fusion style mandatory**: `apply_theme` calls `app.setStyle("Fusion")`. The native Windows style (`windowsvista`) paints native frames for tabs/widgets and partially ignores QSS borders; QSS only becomes authoritative under Fusion.
- **No `font-family` in the sheets** (`design-system.md §1`): the `QApplication` default font is the native OS face. QSS sets sizes and weights only.
- **QSS cannot transition or fade**: hover/focus state changes apply instantly (accepted, `design-system.md §6`). The only animated visuals are the drawer slide and the `SlidingUnderline` widget, both `QPropertyAnimation` driven.
- **QSS box model**: `min-height` / `min-width` exclude the border and `padding` is added inside it. A bar that must measure N px with a 1px border carries `min-height: N-1`. Set a fixed height from a token only through `min-height` on the bar itself.
- **A custom `QWidget` subclass ignores its QSS background** unless `WA_StyledBackground` is set (`Frame`, `SlidingUnderline`, drawer).
- **A dynamic property change needs `repolish(widget)`** (`widget.style().unpolish(widget); widget.style().polish(widget)`); never name a property `size` (collides with `QWidget.size`, use `btnSize`).

## Mandatory internal organization

The example shows the light sheet. The dark sheet has the same rules with the dark values listed after it. Rules below are representative: every widget of the retained composition gets its own named rule (`layout.md §12`).

```qss
/* ============================================================
   styles_[light|dark].qss - [APP_NAME] v[VERSION]
   Theme: [light | dark]
   Reference: design-system.md v2.1 (project palette)
   ============================================================ */

/* --- BASE -------------------------------------------------- */
/* token : bg / text / sm */
QMainWindow, QDialog { background-color: #FFFFFF; }
QWidget { color: #0F181E; font-size: 14px; }

/* --- TOPBAR (N1 chrome) ------------------------------------ */
/* sections mirror the retained composition (layout.md §12) */
/* token : bg-subtle / border / topbar-height (47 + 1px border = 48) / spacing-4 */
QFrame#topbar { background-color: #F1F4F7; border-bottom: 1px solid #D3DAE1;
                min-height: 47px; padding: 0 16px; }

/* --- TABS -------------------------------------------------- */
/* token : text-subtle / primary / border-strong / bg-muted / radius / sm / medium */
/* Style the QTabBar WIDGET, not only ::tab, otherwise the native engine paints its own
   background block. The selected indicator is the SlidingUnderline widget (design-system §8),
   NOT a QSS border-bottom. The transparent 1px border is the hover reservation. */
QTabBar#nav_tabs { background-color: transparent; border: none; }
QTabBar#nav_tabs::tab { background-color: transparent; color: #5A6670; border: 1px solid transparent;
                        border-radius: 5px; padding: 0 16px; min-height: 45px;
                        font-weight: 500; outline: none; }
QTabBar#nav_tabs::tab:selected { color: #3D729E; }                      /* primary (light) */
QTabBar#nav_tabs::tab:hover:!selected { border: 1px solid #6F8192; }    /* border strengthening: transparent -> border-strong */
QTabBar#nav_tabs::tab:pressed { background-color: #E6EBF0; }            /* bg-muted */

/* --- MAIN CONTENT (N0 canvas) ------------------------------ */
/* token : bg / spacing-6 */
QFrame#main_content { background-color: #FFFFFF; }

/* --- PANELS (N2) ------------------------------------------- */
/* token : bg-panel / border / radius */
QFrame[surface="panel"] { background-color: #F1F4F7; border: 1px solid #D3DAE1; border-radius: 5px; }

/* --- LABELS ------------------------------------------------ */
/* token : 2xl / bold / sm / text-subtle / medium / xs / danger-600 */
QLabel[role="section-title"]    { font-size: 24px; font-weight: 700; }
QLabel[role="section-subtitle"] { color: #5A6670; }
QLabel[role="field-label"]      { font-weight: 500; }
QLabel[role="field-error"]      { color: #BA3B52; font-size: 12px; }

/* --- BUTTONS ----------------------------------------------- */
/* token : primary-600/700/800 / text-on-primary / danger-fill/700/800 / border-strong / text / text-subtle
           bg-muted / radius / spacing-1..3 / disabled-* */
/* Every variant carries a 1px border (transparent on Primary, Danger, Ghost): one box, no layout shift. */
QPushButton { border: 1px solid transparent; border-radius: 5px; font-weight: 500; }
QPushButton[btnSize="sm"] { padding: 4px 12px;  font-size: 12px; }
QPushButton[btnSize="md"] { padding: 8px 16px;  font-size: 14px; }
QPushButton[btnSize="lg"] { padding: 12px 24px; font-size: 16px; }

QPushButton[variant="primary"]          { background-color: #3D729E; color: #FFFFFF; }
QPushButton[variant="primary"]:hover    { background-color: #396A93; }   /* primary-700 */
QPushButton[variant="primary"]:pressed  { background-color: #356388; }   /* primary-800 */
QPushButton[variant="primary"]:disabled { background-color: #B1C7D8; color: #FFFFFF; }   /* disabled-primary / disabled-on-primary */
QPushButton[variant="danger"]           { background-color: #BA3B52; color: #FFFFFF; }   /* danger-fill */
QPushButton[variant="danger"]:hover     { background-color: #A23448; }   /* danger-700 */
QPushButton[variant="danger"]:pressed   { background-color: #8A2C3D; }   /* danger-800 */
QPushButton[variant="danger"]:disabled  { background-color: #E3B1BA; color: #FFFFFF; }   /* disabled-danger */
QPushButton[variant="secondary"]          { background-color: transparent; color: #0F181E; border: 1px solid #6F8192; }   /* control edge */
QPushButton[variant="secondary"]:hover    { border: 1px solid #5A6670; }   /* border-strong -> text-subtle */
QPushButton[variant="secondary"]:pressed  { background-color: #E6EBF0; }   /* bg-muted */
QPushButton[variant="secondary"]:disabled { border: 1px solid #C5CDD3; color: #9FA3A5; }   /* disabled-border-strong / disabled-text */
QPushButton[variant="ghost"]          { background-color: transparent; color: #5A6670; }
QPushButton[variant="ghost"]:hover    { border: 1px solid #6F8192; color: #0F181E; }   /* border-strong + text */
QPushButton[variant="ghost"]:pressed  { background-color: #E6EBF0; }   /* bg-muted */
QPushButton[variant="ghost"]:disabled { color: #BDC2C6; }              /* disabled-text-subtle */

/* Focus ring: 2px border INSIDE the box (no outline-offset in QSS), padding shrinks by 1px per side so the size
   never changes. Keyboard only (Qt.TabFocus). Filled buttons use `text`: primary on primary-600 would be 1:1. */
QPushButton[variant="primary"]:focus,
QPushButton[variant="danger"]:focus    { border: 2px solid #0F181E; }   /* text */
QPushButton[variant="secondary"]:focus,
QPushButton[variant="ghost"]:focus     { border: 2px solid #3D729E; }   /* primary */
QPushButton[btnSize="md"]:focus        { padding: 7px 15px; }           /* sm: 3px 11px, lg: 11px 23px */

/* Icon-only button: a QToolButton (a QPushButton keeps a minimum width). Fusion adds 3px, so 6px / 2px
   land on 41px / 29px. */
QToolButton[role="icon"]       { background-color: transparent; border: 1px solid transparent; border-radius: 5px; padding: 6px; }
QToolButton[role="icon"][btnSize="sm"] { padding: 2px; }
QToolButton[role="icon"]:hover   { border: 1px solid #6F8192; }          /* border-strong */
QToolButton[role="icon"]:pressed { background-color: #E6EBF0; }          /* bg-muted */
QToolButton[role="icon"]:focus   { border: 2px solid #3D729E; padding: 5px; }

/* --- PAGINATION -------------------------------------------- */
/* token : text-subtle / border-strong / primary-bg / primary / border-width-emphasis */
QPushButton[role="page"]                { background-color: transparent; color: #5A6670; padding: 0 8px; }
QPushButton[role="page"]:hover          { border: 1px solid #6F8192; }
QPushButton[role="page"][active="true"] { background-color: #EDF3F8; color: #3D729E; border-bottom: 2px solid #3D729E; }

/* --- INPUT FIELDS ------------------------------------------ */
/* token : border-strong / text-subtle / text / primary-600 / danger-600 / spacing-2 / spacing-3 / radius / disabled-* */
/* Focus and error: 2px border without layout shift, padding compensated by 1px. */
QLineEdit { border: 1px solid #6F8192; border-radius: 5px; color: #0F181E; padding: 8px 12px; }
QLineEdit:hover { border: 1px solid #5A6670; }
QLineEdit:focus { border: 2px solid #3D729E; padding: 7px 11px; }
QLineEdit[error="true"] { border: 2px solid #BA3B52; padding: 7px 11px; }
QLineEdit:disabled { border: 1px solid #C5CDD3; color: #9FA3A5; }
/* combobox-popup: 0 is load-bearing under Fusion: applying ANY QSS to a QComboBox flips its popup to the
   Fusion "menu" mode, which crops item height and shows parasitic scroll arrows even for 2 items.
   `combobox-popup: 0` restores the plain list popup. Also style ::item (colour + min-height) or the popup
   items render illegible under Fusion. */
QComboBox { border: 1px solid #6F8192; border-radius: 5px; color: #0F181E; padding: 8px 12px; combobox-popup: 0; }
QComboBox:focus { border: 2px solid #3D729E; padding: 7px 11px; }
QComboBox QAbstractItemView { background-color: #FFFFFF; color: #0F181E; border: 1px solid #6F8192; outline: 0; }   /* bg-elevated / border-strong */
QComboBox QAbstractItemView::item { color: #0F181E; padding: 6px 10px; min-height: 24px; }

/* --- TABLES ------------------------------------------------ */
/* token : bg / bg-subtle / text-subtle / border-strong / border-subtle / primary-bg / primary / semibold */
/* The 2px selection bar is painted by SelectionBarDelegate (QSS cannot paint a single edge on item views). */
QTableView#data_table { background-color: #FFFFFF; border: none; gridline-color: #E3E8ED; }
QTableView#data_table::item { padding: 8px 12px; border-bottom: 1px solid #E3E8ED; }
QTableView#data_table::item:selected { background-color: #EDF3F8; color: #3D729E; }   /* primary-bg / primary */
QTableView#data_table::item:hover { background-color: #F1F4F7; }   /* bg-subtle: secondary cue on wide rows */
QTableView#data_table::item:focus { border: 2px solid #3D729E; }   /* ring inset on the item */
QHeaderView::section { background-color: #F1F4F7; color: #5A6670; font-weight: 600; border: none;
                       border-bottom: 2px solid #6F8192; padding: 8px 12px; }

/* --- TREE -------------------------------------------------- */
/* token : primary-bg / primary / text-subtle / spacing-1 / spacing-4 */
/* Chevrons are recolored SVG files: the placeholder is replaced at load by utils/styles.py (icon_file()). */
QTreeView#tree::branch:has-children:closed { image: url({{icon:chevron-right:default}}); }
QTreeView#tree::branch:has-children:open   { image: url({{icon:chevron-down:default}}); }
QTreeView#tree::item { padding: 4px 0; border: 1px solid transparent; }
QTreeView#tree::item:hover { border: 1px solid #6F8192; }
QTreeView#tree::item:selected { background-color: #EDF3F8; color: #3D729E; }

/* --- SIDEBAR / MASTER LIST (N1 chrome) --------------------- */
/* token : bg-subtle / border / text-subtle / primary / medium; rows are widgets in a FittedList */
QFrame#sidebar { background-color: #F1F4F7; border-right: 1px solid #D3DAE1; }
QLabel[role="nav-label"] { color: #5A6670; font-weight: 500; }
QLabel[role="nav-label"][selected="true"] { color: #3D729E; }
QListWidget#master_list { background-color: #F1F4F7; border: none; }

/* --- MENU BAR (P3, native QMenuBar) ------------------------- */
/* token : bg-subtle / border / bg-muted / border-strong / bg-elevated / menu-min-width / text-muted
   Do NOT set min-height / max-height on QMenuBar: it is added to the items and pushes them into the overflow. */
QMenuBar#menu_bar { background-color: #F1F4F7; border-bottom: 1px solid #D3DAE1; padding: 3px; }
QMenuBar#menu_bar::item { padding: 4px 12px; border: 1px solid transparent; border-radius: 5px; font-weight: 500; }
QMenuBar#menu_bar::item:hover { border: 1px solid #6F8192; }
QMenuBar#menu_bar::item:pressed { background-color: #E6EBF0; }   /* open label: bg-muted */
QMenu { background-color: #FFFFFF; border: 1px solid #6F8192; border-radius: 5px; min-width: 200px; }
QMenu::item { padding: 8px 16px; border: 1px solid transparent; border-radius: 3px; }   /* nested radius */
QMenu::item:selected { border: 1px solid #6F8192; }
QMenu::item:disabled { color: #98A4AE; }   /* text-muted */
QMenu::separator { height: 1px; background-color: #E3E8ED; }   /* border-subtle */

/* --- STATUSBAR (N1, one step darker) ------------------------ */
/* token : bg-muted / border / text-subtle / statusbar-height (27 + 1px border = 28) / xs */
/* Statusbar text = text-subtle (NOT text-muted): design-system.md §12, layout.md §7. */
QStatusBar#statusbar { background-color: #E6EBF0; border-top: 1px solid #D3DAE1; min-height: 27px;
                       padding: 0 16px; font-size: 12px; color: #5A6670; }

/* --- TOAST ------------------------------------------------- */
/* token : *-50 / *-600 / border-width-accent / radius */
QFrame#toast[tone="success"] { background-color: #EFF6F3; border-left: 4px solid #328F6D; border-radius: 5px; }
QFrame#toast[tone="warning"] { background-color: #F8F5EC; border-left: 4px solid #A58327; border-radius: 5px; }
QFrame#toast[tone="danger"]  { background-color: #F8EFF1; border-left: 4px solid #BA3B52; border-radius: 5px; }
QFrame#toast[tone="info"]    { background-color: #EDF3F8; border-left: 4px solid #3D729E; border-radius: 5px; }   /* info = accent */

/* --- DRAWER / MODAL (N3 floating) --------------------------- */
/* token : bg-elevated / border-strong / radius / spacing-6 / overlay / modal-min-width */
QFrame#drawer { background-color: #FFFFFF; border-left: 1px solid #6F8192; padding: 24px; }
QWidget#drawer_overlay, QDialog#modal_overlay { background-color: rgba(15, 24, 30, 102); }   /* overlay: text at alpha 0.4 */
QFrame#modal { background-color: #FFFFFF; border: 1px solid #6F8192; border-radius: 5px; min-width: 480px; padding: 24px; }

/* --- SCROLLBARS -------------------------------------------- */
/* token : bg-muted / border-strong / radius */
QScrollBar:vertical   { background: transparent; width: 12px; margin: 0; }
QScrollBar:horizontal { background: transparent; height: 12px; margin: 0; }
QScrollBar::handle:vertical,
QScrollBar::handle:horizontal        { background: #E6EBF0; border-radius: 5px; min-height: 24px; min-width: 24px; }
QScrollBar::handle:hover             { background: #6F8192; }   /* border-strong */
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }   /* no arrows */
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

/* --- TOOLTIP ----------------------------------------------- */
/* token : text on bg-elevated (17.95:1 light, 13.43:1 dark) / border-strong / radius / xs */
QToolTip { background-color: #FFFFFF; color: #0F181E; border: 1px solid #6F8192;
           border-radius: 5px; padding: 4px 8px; font-size: 12px; }

/* --- SELECTION (text) -------------------------------------- */
/* token : selection-bg (primary-50) / selection-text (text) */
QLineEdit, QTextEdit, QPlainTextEdit {
    selection-background-color: #EDF3F8;
    selection-color: #0F181E;
}
```

> Dark sheet values (Steel Blue default, derived; same rules): `bg` `#111519`, `bg-subtle` `#1A2025`, `bg-muted` `#2B343C`, `bg-elevated` / `bg-panel` `#222930` (modal, drawer, menu panel, tooltip, combo popup), `text` `#F2F5F7`, `text-subtle` `#A3AEB8`, `text-muted` `#5F6C77`, `border` `#3A444D`, `border-subtle` `#2A333A`, `border-strong` `#768A9B`. Foreground accent (active tab text, focus ring on Secondary/Ghost/fields, selected row text, icon) is `primary-400` `#91B6D4`; selected background `primary-900` `#24425C`; toast info = `#24425C` with a `#91B6D4` edge. Primary fill stays `primary-600` `#3D729E` (hover `#396A93`, pressed `#356388`) with white text, and the Danger fill stays the light `danger-fill` `#BA3B52` (hover `#A23448`, pressed `#8A2C3D`); the dark `#CB7282` is the foreground danger (field error, toast edge). Toasts: `#26372F` / `#6EC4A4`, `#392F1B` / `#D2B460`, `#38222B` / `#CB7282`. Disabled (pre-blended over `bg`): `disabled-text` `#6B6F72`, `disabled-text-subtle` `#4B5259`, `disabled-border-strong` `#39444D`, `disabled-primary` `#233A4E`, `disabled-danger` `#552430`, `disabled-on-primary` `#707375`. Overlay `rgba(242, 245, 247, 102)`. Ring on filled buttons stays `text` (`#F2F5F7`).

## Reference tokens (design-system.md v2.1 - default Steel Blue palette, derived)

### Light mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #FFFFFF |
| `bg-subtle`     | #F1F4F7 |
| `bg-muted`      | #E6EBF0 |
| `bg-elevated`   | #FFFFFF |
| `bg-panel`      | #F1F4F7 |
| `text`          | #0F181E |
| `text-subtle`   | #5A6670 |
| `text-muted`    | #98A4AE |
| `border`        | #D3DAE1 |
| `border-subtle` | #E3E8ED |
| `border-strong` | #6F8192 |
| `primary-50`    | #EDF3F8 |
| `primary-600`   | #3D729E |
| `primary-700`   | #396A93 |
| `primary-800`   | #356388 |

### Dark mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #111519 |
| `bg-subtle`     | #1A2025 |
| `bg-elevated`   | #222930 |
| `bg-muted`      | #2B343C |
| `bg-panel`      | #222930 |
| `text`          | #F2F5F7 |
| `text-subtle`   | #A3AEB8 |
| `text-muted`    | #5F6C77 |
| `border`        | #3A444D |
| `border-subtle` | #2A333A |
| `border-strong` | #768A9B |
| `primary-400`   | #91B6D4 |
| `primary-600`   | #3D729E |
| `primary-700`   | #396A93 |
| `primary-800`   | #356388 |
| `primary-900`   | #24425C |
| `text-on-primary` | #FFFFFF |

Semantic values (both themes): `design-system.md §2` (derived per project; the defaults above pair with `success-600` #328F6D/#6EC4A4, `warning-600` #A58327/#D2B460, `danger-600` #BA3B52/#CB7282, `danger-fill` #BA3B52 in both themes, info = accent). Disabled colors and overlay: `design-system.md §2` ("Disabled colors and overlay").

### Depth by stroke and surface ladder (non-negotiable)

- `border-radius: 5px` on every rounded element (buttons, fields, toasts, modals, scrollbar handles); nested elements (menu items inside a 5px container) use 3px. Never another radius value.
- No shadow (`box-shadow`, `QGraphicsDropShadowEffect`). No gradient.
- Four levels (`design-system.md §2`): N0 canvas `bg`; N1 chrome `bg-subtle` (topbar, menu bar, sidebar, master list) and statusbar `bg-muted`; N2 panels `bg-panel`; N3 floating layers `bg-elevated` with a `border-strong` edge (drawer, modal, menu panel, tooltip). Never put a topbar, menu bar or footer on `bg`.
- A control's edge (field, Secondary button) is `border-strong` (3:1); `border` is a decorative separator only.

### Focus indicator

- `outline-offset` does not exist in QSS. The ring is the widget's own border, drawn **inside**: 1px default border -> 2px on `:focus`, padding reduced by 1px per side so the size never changes.
- Ring color: `primary` (light `primary-600`, dark `primary-400`); on Primary and Danger buttons it is `text` (3:1 against the fill).
- Qt has no `:focus-visible`: buttons, icon buttons and tab bars use `Qt.FocusPolicy.TabFocus` (keyboard only); text inputs show the ring on any focus. Item views draw the ring inset with `::item:focus`.
- Never remove the ring (`QWidget:focus { border: none; }` is forbidden).

### Hover - border strengthening

- Neutral interactive elements hover by **stroke**, not fill (`design-system.md §8`): the default state carries a transparent 1px border; on hover it becomes `border-strong` (3:1). A bordered control (`border-strong`) climbs to `text-subtle`. Instant (QSS cannot transition).
- `pressed` keeps the `bg-muted` fill (transient feedback). Wide table rows strengthen their bottom border and may add `bg-subtle` as a secondary cue.

### Selection - never by color alone

- Selected item: `primary-bg` background, `primary` text and a 2px `primary` bar on the leading edge, painted by `SelectionBarDelegate` on column 0 of item views (`border-left` on `::item` would shift the content). Pagination uses a 2px `border-bottom` on `[active="true"]`.
- Tabs: the `SlidingUnderline` widget (`views/sliding_underline.py`, `design-system.md §8`), **not** a QSS `border-bottom`. QSS gives the tab row its base styling only. Keep `setDrawBase(False)` on the `QTabBar`.

### Item views that host widgets

`setItemWidget` rows (sidebar, master list) get their height from the widget layout, not from QSS padding (QSS padding is not part of the delegate `sizeHint`). Use `FittedList` (`views/base.py`), which recomputes the size hints in `resizeEvent` and `showEvent`. Wrapping text in an item view is a row widget with a wrapping `QLabel`, never `setWordWrap` on the item.

### Not reachable from QSS (and the substitute)

| Need | Substitute |
| ---- | ---------- |
| CSS variables, `rem` | literal hex and px, each rule commented with its token |
| `opacity` | pre-blended `disabled-*` and `overlay` literals |
| `transition` | state changes are instant; `QPropertyAnimation` for the underline and the drawer |
| `outline`, `outline-offset`, `:focus-visible` | inset 2px border, `Qt.TabFocus` |
| Single-edge selection bar on item views | `SelectionBarDelegate` |
| `line-height` | margins, `QTextOption` |
| Recolored image in `url()` | recolored SVG file via the `{{icon:NAME:KEY}}` placeholder, replaced by `utils/styles.py` at load (the only placeholder left in the committed sheets) |
| `inert` | `InertScope` (`utils/a11y.py`) behind the drawer; `QDialog` modality for modals |
| Native roles (placeholder text, tooltip base, sort arrow, disabled text of unstyled widgets, native popups, window frame) | `QPalette` from `config.NATIVE_PALETTE` and `QStyleHints.setColorScheme`, both applied with the sheet by `apply_theme` |

## Per-project palette

In Phase 1 the project picks a **palette** (named or custom): the accent is mandatory (-> `primary-600` after the AA darkening), the four other roles are optional overrides (main background -> `bg`, secondary background -> `bg-subtle`, text -> `text`, details -> `border`). Claude derives everything else (`design-system.md §2`): the accent stops, `text-on-primary`, the **accent-tinted neutrals** and the surface ladder for both themes, the **per-project semantic colors** (hue anchors harmonized ±6° toward the accent; info = accent; `danger-fill`), and the pre-blended `disabled-*` colors, then writes the resolved hex into **both** `styles_light.qss` and `styles_dark.qss` (+ accent stops, `ICON_COLORS`, `ON_PRIMARY`, `NATIVE_PALETTE`, and `SPLASH_COLORS` if the splash is on, in `config.py`). An explicit override wins over the tinted target for its token; its supporting tokens derive from it. The values above are the **default palette**: a custom palette replaces them throughout both sheets. The global `design-system.md` stays unchanged (it documents the rule, not the per-project values).

## Anti-patterns - what NOT to do

- **Do not** set a color/size/font directly in Python (`setStyleSheet("...")` inline, `QColor(...)` for a themed value). Route it through the QSS sheets + an `objectName` or a dynamic property. Documented exceptions: `config.PRIMARY_*` / `ON_PRIMARY` / `ICON_COLORS` / `NATIVE_PALETTE` / `SPLASH_COLORS`, the `SlidingUnderline` widget and the `SelectionBarDelegate` reading `config.PRIMARY_*` (`design-system.md §11`).
- **Do not** write a QSS value without a `/* token : ... */` comment tracing to `design-system.md`.
- **Do not** handle dark mode with a `[theme]`-conditional single sheet or partial override: replace the whole sheet through `apply_theme`.
- **Do not** use a radius other than 5px (or 3px nested), and never add `box-shadow`, `QGraphicsDropShadowEffect`, or a gradient: depth is stroke-based.
- **Do not** style a widget without an `objectName` or a dynamic property (no generic class selector when a named rule is expected).
- **Do not** change a dynamic property without `repolish`, and **do not** name one `size`.
- **Do not** style a `QTabBar` only via `::tab`: also set the `QTabBar` widget background to `transparent`, add `outline: none` on `::tab`, and `setDrawBase(False)`. The selected indicator is the `SlidingUnderline` widget, never a QSS `border-bottom`. **Root cause of persistent left/right/top borders on Windows: the native `windowsvista` style**; none of the QSS above works until `app.setStyle("Fusion")` is applied. Verify in both themes on a real Windows machine (the offscreen platform does not use `windowsvista`).
- **Do not** hover by `bg-muted` fill on a neutral element: hover is border strengthening (§8); `bg-muted` is the `pressed` feedback.
- **Do not** put icon colors in QSS: Lucide icon colors live in `config.py` (`ICON_COLORS`), consumed by `utils/icons.py` (documented exception).
- **Do not** put splash colors in QSS: a `QSplashScreen` is painted programmatically, so its `bg`/`text` live in `config.py` (`SPLASH_COLORS`), a documented exception (only when the splash screen is on, Phase 3). See `@rules/splash.md`.
- **Do not** use `opacity` or an `rgba` alpha for a disabled state: use the pre-blended `disabled-*` literals. The only alpha allowed is the `overlay` scrim.
- **Do not** set `min-height` / `max-height` on `QMenuBar`, and do not size item-view rows from QSS padding (use `FittedList`).
- **Do not** put a Primary or Danger focus ring in `primary` (1:1 against the fill): it is `text`.
- **Do not** pin a `font-family` in the sheets: the QApplication system font is the face (`design-system.md §1`).

## Integrity verification

Detailed in `@rules/verification.md`. Key points: zero hardcoded visual value in Python (no inline `setStyleSheet`, no themed `QColor`) - the documented exceptions are `PRIMARY_*` / `ON_PRIMARY` / `ICON_COLORS` / `NATIVE_PALETTE`, `SPLASH_COLORS` if the splash is on, the `SlidingUnderline` widget and the `SelectionBarDelegate`; both sheets `resources/styles_light.qss` + `resources/styles_dark.qss` present, dark mode = full sheet replacement through a single `apply_theme` (Fusion, color scheme, `QPalette`, sheet); every styled widget carries an `objectName` or a dynamic property matching a named rule, every QSS rule carries its `/* token : ... */` comment, every property change is followed by `repolish`; stroke-based depth held (radius 5px/3px only, no shadow, no gradient, hover by border strengthening to `border-strong`, floating layers on `bg-elevated` + `border-strong`, chrome on `bg-subtle`); control edge on `border-strong`; focus ring drawn inside the widget (`text` on filled buttons), `Qt.TabFocus` on buttons and tab bars, never removed; selected state never by color alone (2px bar from `SelectionBarDelegate`, tab underline); statusbar text = `text-subtle`; tabs indicator = `SlidingUnderline`, no QSS selected border-bottom; custom `QWidget` subclasses set `WA_StyledBackground`; disabled states use the `disabled-*` literals.
