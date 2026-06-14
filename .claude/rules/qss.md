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
   Reference: design-system.md v1.1
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
/* token : primary-600 / border / text / danger-600 / text-subtle */
QPushButton#btn_primary   { background-color: #4F46E5; color: #FFFFFF; border: none; }
QPushButton#btn_secondary { background-color: transparent; color: #111827; border: 1px solid #E5E7EB; }
QPushButton#btn_danger    { background-color: #DC2626; color: #FFFFFF; border: none; }
QPushButton#btn_ghost     { background-color: transparent; color: #6B7280; border: none; }

/* --- INPUT FIELDS ------------------------------------------ */
/* token : border / text / spacing-2 / spacing-3 */
QLineEdit { border: 1px solid #E5E7EB; color: #111827; padding: 8px 12px; }
QLineEdit:focus { border: 2px solid #4F46E5; }
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
QDialog { background-color: #FFFFFF; border: 1px solid #E5E7EB; }
```

## Reference tokens (design-system.md v1.1)

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

### Dark mode

| Token           | Value   |
| --------------- | ------- |
| `bg`            | #111827 |
| `bg-subtle`     | #1F2937 |
| `bg-muted`      | #1F2937 |
| `bg-elevated`   | #374151 |
| `text`          | #F9FAFB |
| `text-subtle`   | #9CA3AF |
| `text-muted`    | #6B7280 |
| `border`        | #374151 |
| `border-subtle` | #1F2937 |
| `border-strong` | #4B5563 |
| `primary-400`   | #818CF8 |
| `primary-900`   | #312E81 |

### Flat design (non-negotiable)

- `border-radius`: 0px on all widgets.
- No shadow (`box-shadow`, `QGraphicsDropShadowEffect`).
- No gradient.

## Per-project primary color

If a color was chosen in Phase 1 (≠ Slate Blue): only the 4 `primary-50/400/600/900` values change in the project's `styles_*.qss` and `config.py`. The global `design-system.md` stays unchanged.

## Anti-patterns — what NOT to do

- **Do not** set a color/size/font directly in Python (`setStyleSheet("...")` inline, `QColor(...)` for a themed value). Route it through the QSS sheets + an `objectName`.
- **Do not** write a QSS value without a `/* token : ... */` comment tracing to `design-system.md`.
- **Do not** handle dark mode with a `[theme]`-conditional single sheet or partial override — replace the whole sheet.
- **Do not** add `border-radius`, `box-shadow`, `QGraphicsDropShadowEffect`, or a gradient — flat design is global.
- **Do not** style a widget without giving it an `objectName` (or use a generic class selector when a named rule is expected).
- **Do not** put icon colors in QSS — qtawesome colors live in `config.py` (`ICON_COLORS`), the one documented exception.
