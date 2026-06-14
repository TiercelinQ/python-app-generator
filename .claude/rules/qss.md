# QSS and styles rules

## Principles

- Zero hardcoded visual value in Python. Everything in `styles_light.qss` / `styles_dark.qss` or `config.py`.
- Every styled widget has an `objectName` matching a named QSS rule.
- Every QSS rule carries a `/* token : [name] */` comment tracing to `design-system.md`.
- Dark mode: complete sheet replacement (`styles_light.qss` → `styles_dark.qss`). Never a partial override.
- **Two mandatory files**: `resources/styles_light.qss` + `resources/styles_dark.qss`. No single conditional file.

## Mandatory internal organization

```qss
/* ============================================================
   styles_[light|dark].qss — [APP_NAME] v[VERSION]
   Theme: [light | dark]
   Reference: design-system.md v1.2
   ============================================================ */

/* --- BASE -------------------------------------------------- */
/* token : bg / text */
QMainWindow { background-color: #FFFFFF; color: #111827; }

/* --- TOPBAR ------------------------------------------------ */
/* token : bg / border / topbar-height */
QWidget#topbar { background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;
                 min-height: 48px; max-height: 48px; padding: 0 16px; }

/* --- TABS -------------------------------------------------- */
/* token : text-subtle / primary-600 / bg-muted / topbar-height */
QTabBar::tab { ... }
QTabBar::tab:selected { color: #4F46E5; border-bottom: 2px solid #4F46E5; }
QTabBar::tab:hover { background-color: #F3F4F6; }

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
QPushButton#btn_primary           { background-color: #4F46E5; color: #FFFFFF; border: none; }
QPushButton#btn_primary:hover     { background-color: #4338CA; }   /* primary-700 */
QPushButton#btn_primary:pressed   { background-color: #3730A3; }   /* primary-800 */
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
QLineEdit:focus { border: 2px solid #4F46E5; padding: 7px 11px; }
QComboBox { ... }

/* --- TABLES ------------------------------------------------ */
/* token : bg-subtle / text-subtle / border-strong / border-subtle / primary-50 / bg-muted */
QTableView { border: none; gridline-color: #F3F4F6; }
QHeaderView::section { background-color: #F9FAFB; border-bottom: 2px solid #D1D5DB; }
QTableView::item:selected { background-color: #EEF2FF; }
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
    selection-background-color: #EEF2FF;   /* selection-bg light */
    selection-color: #111827;              /* selection-text light */
}
```

> Dark sheet equivalents: scrollbar handle `#374151` (bg-muted), hover `#4B5563` (border-strong); tooltip bg `#374151` (bg-muted), color `#F9FAFB`, border `#4B5563` (border-strong); selection bg `#312E81` (primary-900), color `#F9FAFB`; disabled `rgba(249, 250, 251, 0.4)`.
>
> Dark toast backgrounds (`*-50` dark role tint): `toast_success` `#14532D`, `toast_warning` `#78350F`, `toast_danger` `#7F1D1D`, `toast_info` `#1E3A8A`; left borders use the `*-600` dark accents (`#4ADE80` / `#FCD34D` / `#F87171` / `#60A5FA`). Toast message text uses `text` (`#F9FAFB` dark).

## Reference tokens (design-system.md v1.2)

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
| `primary-50`    | #EEF2FF |
| `primary-600`   | #4F46E5 |
| `primary-700`   | #4338CA |
| `primary-800`   | #3730A3 |

### Dark mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #111827 |
| `bg-subtle`     | #1F2937 |
| `bg-elevated`   | #1F2937 |
| `bg-muted`      | #374151 |
| `text`          | #F9FAFB |
| `text-subtle`   | #9CA3AF |
| `text-muted`    | #6B7280 |
| `border`        | #374151 |
| `border-subtle` | #1F2937 |
| `border-strong` | #4B5563 |
| `primary-400`   | #818CF8 |
| `primary-700`   | #4338CA |
| `primary-800`   | #3730A3 |
| `primary-900`   | #312E81 |

### Flat design (non-negotiable)

- `border-radius`: 0px on all widgets.
- No shadow (`box-shadow`, `QGraphicsDropShadowEffect`).
- No gradient.

### Focus indicator

- `outline-offset` is not reliable in QSS. Show focus with a 2px border in the focus color, compensating padding so the layout does not shift (see the input-field example: 1px/8-12px default → 2px/7-11px on `:focus`).
- Light: `primary-600`. Dark: `primary-400`. Never remove the focus indicator.

## Per-project primary color

If a color was chosen in Phase 1 (≠ Slate Blue): only the 6 `primary-50/400/600/700/800/900` values change in the project's `styles_*.qss` and `config.py`. The global `design-system.md` stays unchanged.

## Anti-patterns — what NOT to do

- **Do not** set a color/size/font directly in Python (`setStyleSheet("...")` inline, `QColor(...)` for a themed value). Route it through the QSS sheets + an `objectName`.
- **Do not** write a QSS value without a `/* token : ... */` comment tracing to `design-system.md`.
- **Do not** handle dark mode with a `[theme]`-conditional single sheet or partial override — replace the whole sheet.
- **Do not** add `border-radius`, `box-shadow`, `QGraphicsDropShadowEffect`, or a gradient — flat design is global.
- **Do not** style a widget without giving it an `objectName` (or use a generic class selector when a named rule is expected).
- **Do not** put icon colors in QSS — qtawesome colors live in `config.py` (`ICON_COLORS`), the one documented exception.
