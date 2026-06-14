# QSS and styles rules

## Principles

- Zero hardcoded visual value in Python. Everything in `styles_light.qss` / `styles_dark.qss` or `config.py`.
- Every styled widget has an `objectName` matching a named QSS rule.
- Every QSS rule carries a `/* token : [name] */` comment tracing to `design-system.md`.
- Dark mode: complete sheet replacement (`styles_light.qss` → `styles_dark.qss`). Never a partial override.
- **Two mandatory files**: `resources/styles_light.qss` + `resources/styles_dark.qss`. No single conditional file.
- **Fusion style mandatory** in `main.py`: `app.setStyle("Fusion")` right after `QApplication(sys.argv)`. The native Windows style (`windowsvista`) paints native frames for tabs/widgets and partially ignores QSS borders — QSS only becomes authoritative under Fusion. Without it, flat styling (e.g. `QTabBar` borders) renders wrong on Windows.

## Mandatory internal organization

```qss
/* ============================================================
   styles_[light|dark].qss — [APP_NAME] v[VERSION]
   Theme: [light | dark]
   Reference: design-system.md v1.3
   ============================================================ */

/* --- BASE -------------------------------------------------- */
/* token : bg / text */
QMainWindow { background-color: #FFFFFF; color: #111827; }

/* --- TOPBAR ------------------------------------------------ */
/* token : bg / border / topbar-height */
QWidget#topbar { background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;
                 min-height: 48px; max-height: 48px; padding: 0 16px; }

/* --- TABS -------------------------------------------------- */
/* token : bg / text-subtle / primary-600 / bg-muted / topbar-height */
/* Style the QTabBar WIDGET, not only ::tab — otherwise the native engine paints
   its own background block behind the tabs (grey/blue, not matching the topbar). */
QTabBar#nav_tabs { background-color: transparent; border: none; }
/* outline:none removes the native focus rectangle (left/right/top borders on the
   active tab); the transparent border-bottom reserves the underline space so the
   layout does not shift on selection. */
QTabBar::tab { background-color: transparent; border: none;
               border-bottom: 2px solid transparent; outline: none; }
QTabBar::tab:selected { color: #4682B4; border: none; border-bottom: 2px solid #4682B4; }
QTabBar::tab:hover:!selected { background-color: #F3F4F6; }

/* --- MAIN CONTENT ------------------------------------------ */
/* token : bg / spacing-6 */
QWidget#main_content { background-color: #FFFFFF; padding: 24px; }

/* --- TOAST ------------------------------------------------- */
/* token : success-50 / success-600 / spacing-3 / spacing-4 */
QWidget#toast_success { background-color: #F0FDF4; border-left: 4px solid #16A34A; }
QWidget#toast_warning { background-color: #FFFBEB; border-left: 4px solid #D97706; }
QWidget#toast_danger  { background-color: #FFF1F2; border-left: 4px solid #DC2626; }
QWidget#toast_info    { background-color: #EFF6FF; border-left: 4px solid #2563EB; }

/* --- BUTTONS ----------------------------------------------- */
/* token : primary-600/700/800 / border / text / danger-600/700/800 / text-subtle / bg-muted */
QPushButton#btn_primary           { background-color: #4682B4; color: #FFFFFF; border: none; }
QPushButton#btn_primary:hover     { background-color: #396A93; }   /* primary-700 */
QPushButton#btn_primary:pressed   { background-color: #2F5879; }   /* primary-800 */
QPushButton#btn_secondary         { background-color: transparent; color: #111827; border: 1px solid #E5E7EB; }
QPushButton#btn_secondary:hover   { background-color: #F3F4F6; }   /* bg-muted */
QPushButton#btn_secondary:pressed { background-color: #F3F4F6; }
QPushButton#btn_danger            { background-color: #DC2626; color: #FFFFFF; border: none; }
QPushButton#btn_danger:hover      { background-color: #B91C1C; }   /* danger-700 */
QPushButton#btn_danger:pressed    { background-color: #991B1B; }   /* danger-800 */
QPushButton#btn_ghost             { background-color: transparent; color: #6B7280; border: none; }
QPushButton#btn_ghost:hover       { background-color: #F3F4F6; }   /* bg-muted */
QPushButton:disabled              { color: rgba(17, 24, 39, 0.4); }   /* opacity-disabled 40% */

/* --- INPUT FIELDS ------------------------------------------ */
/* token : border / text / primary-600 / spacing-2 / spacing-3 */
/* Focus: 2px border without layout shift — compensate padding by 1px on :focus */
QLineEdit { border: 1px solid #E5E7EB; color: #111827; padding: 8px 12px; }
QLineEdit:focus { border: 2px solid #4682B4; padding: 7px 11px; }
QComboBox { ... }

/* --- TABLES ------------------------------------------------ */
/* token : bg-subtle / text-subtle / border-strong / border-subtle / primary-50 / bg-muted */
QTableView { border: none; gridline-color: #F3F4F6; }
QHeaderView::section { background-color: #F9FAFB; border-bottom: 2px solid #D1D5DB; }
QTableView::item:selected { background-color: #EDF3F8; }
QTableView::item:hover { background-color: #F3F4F6; }

/* --- STATUSBAR --------------------------------------------- */
/* token : bg-muted / border / text-muted / statusbar-height / xs */
QStatusBar { background-color: #F3F4F6; border-top: 1px solid #E5E7EB;
             min-height: 28px; max-height: 28px; padding: 0 16px;
             font-size: 12px; color: #9CA3AF; }

/* --- DRAWER ------------------------------------------------ */
/* token : bg-elevated / border / spacing-6 */
QWidget#drawer { background-color: #FFFFFF; border-left: 1px solid #E5E7EB; padding: 24px; }

/* --- DIALOG / MODAL ---------------------------------------- */
/* token : bg / border / spacing-6 */
QDialog { background-color: #FFFFFF; border: 1px solid #E5E7EB; min-width: 480px; }

/* --- SCROLLBARS (flat) ------------------------------------- */
/* token : bg-muted / border-strong */
QScrollBar:vertical   { background: transparent; width: 12px; margin: 0; }
QScrollBar:horizontal { background: transparent; height: 12px; margin: 0; }
QScrollBar::handle:vertical,
QScrollBar::handle:horizontal        { background: #F3F4F6; min-height: 24px; min-width: 24px; }
QScrollBar::handle:hover             { background: #D1D5DB; }   /* border-strong */
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }   /* no arrows */
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

/* --- TOOLTIP ----------------------------------------------- */
/* token : text (inverted bg) / bg / border / spacing-2 / xs */
QToolTip { background-color: #111827; color: #FFFFFF; border: 1px solid #E5E7EB;
           padding: 4px 8px; font-size: 12px; }

/* --- SELECTION (text) -------------------------------------- */
/* token : primary-50 / text */
QLineEdit, QTextEdit, QPlainTextEdit {
    selection-background-color: #EDF3F8;   /* selection-bg light */
    selection-color: #111827;              /* selection-text light */
}
```

> Dark sheet equivalents: scrollbar handle `#313140` (bg-muted), hover `#4A4A5E` (border-strong); tooltip bg `#313140` (bg-muted), color `#D4D4D4`, border `#4A4A5E` (border-strong); selection bg `#2A4F72` (primary-900), color `#D4D4D4`; disabled `rgba(212, 212, 212, 0.4)`.
>
> Dark toast backgrounds (`*-50` dark role tint): `toast_success` `#1D3F2A`, `toast_warning` `#483B13`, `toast_danger` `#441818`, `toast_info` `#1A3042`; left borders use the `*-600` dark accents (`#4A9E6A` / `#CCA840` / `#C04A4A` / `#4682B4`). Toast message text uses `text` (`#D4D4D4` dark).
>
> Dark buttons: `btn_primary` base stays `#4682B4` (primary-600, identical in both sheets), hover `#396A93` / pressed `#2F5879`. `btn_danger` base becomes `#C04A4A` (danger-600 **dark**), hover `#B91C1C` / pressed `#991B1B` (danger-700/800, mode-agnostic). White text keeps AA on both (`#4682B4` 4.11:1, `#C04A4A` 4.86:1).

## Reference tokens (design-system.md v1.3)

### Light mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #FFFFFF |
| `bg-subtle`     | #F9FAFB |
| `bg-muted`      | #F3F4F6 |
| `bg-elevated`   | #FFFFFF |
| `text`          | #111827 |
| `text-subtle`   | #6B7280 |
| `text-muted`    | #9CA3AF |
| `border`        | #E5E7EB |
| `border-subtle` | #F3F4F6 |
| `border-strong` | #D1D5DB |
| `primary-50`    | #EDF3F8 |
| `primary-600`   | #4682B4 |
| `primary-700`   | #396A93 |
| `primary-800`   | #2F5879 |

### Dark mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #1A1A1F |
| `bg-subtle`     | #22222A |
| `bg-elevated`   | #2A2A35 |
| `bg-muted`      | #313140 |
| `text`          | #D4D4D4 |
| `text-subtle`   | #9A9AB0 |
| `text-muted`    | #5A5A72 |
| `border`        | #3A3A4A |
| `border-subtle` | #2E2E3A |
| `border-strong` | #4A4A5E |
| `primary-400`   | #5A9FD4 |
| `primary-700`   | #396A93 |
| `primary-800`   | #2F5879 |
| `primary-900`   | #2A4F72 |

### Flat design (non-negotiable)

- `border-radius`: 0px on all widgets.
- No shadow (`box-shadow`, `QGraphicsDropShadowEffect`).
- No gradient.

### Focus indicator

- `outline-offset` is not reliable in QSS. Show focus with a 2px border in the focus color, compensating padding so the layout does not shift (see the input-field example: 1px/8-12px default → 2px/7-11px on `:focus`).
- Light: `primary-600`. Dark: `primary-400`. Never remove the focus indicator.

## Per-project primary color

If a color was chosen in Phase 1 (≠ Steel Blue): only the 6 `primary-50/400/600/700/800/900` values change in the project's `styles_*.qss` and `config.py`. The global `design-system.md` stays unchanged.

## Anti-patterns — what NOT to do

- **Do not** set a color/size/font directly in Python (`setStyleSheet("...")` inline, `QColor(...)` for a themed value). Route it through the QSS sheets + an `objectName`.
- **Do not** write a QSS value without a `/* token : ... */` comment tracing to `design-system.md`.
- **Do not** handle dark mode with a `[theme]`-conditional single sheet or partial override — replace the whole sheet.
- **Do not** add `border-radius`, `box-shadow`, `QGraphicsDropShadowEffect`, or a gradient — flat design is global.
- **Do not** style a widget without giving it an `objectName` (or use a generic class selector when a named rule is expected).
- **Do not** style a `QTabBar` only via `::tab` — also set the `QTabBar` widget background to `transparent`, add `outline: none` on `::tab`, and `setDrawBase(False)` on the widget. Selected tab: `border: none` + `border-bottom` only. **Root cause of persistent left/right/top borders on Windows: the native `windowsvista` style** — none of the QSS above works until `app.setStyle("Fusion")` is set in `main.py`. Verify in both themes on a real Windows machine (the offscreen platform does not use `windowsvista`).
- **Do not** put icon colors in QSS — qtawesome colors live in `config.py` (`ICON_COLORS`), the one documented exception.
