# Design System — v1.1

> Binding reference for all Python/PyQt6 applications.
> Use: Windows desktop applications, personal and professional use.
> Inseparable from `layout.md`.

## Changelog

| Version | Date       | Main change                                                   |
| ------- | ---------- | ------------------------------------------------------------- |
| v1.1    | 2026-06-12 | QSS 2 mandatory files · primary-* HSL derivation rule         |
| v1.0    | initial    | Typography, colors, spacing, components, states               |

Every generated application references the active version in its `README.md`.

---

## 1. TYPOGRAPHY

| Token         | Value    | Usage                         |
| ------------- | -------- | ----------------------------- |
| `font-family` | Segoe UI | All applications              |
| `xs`          | 12px     | Statusbar, secondary labels   |
| `sm`          | 14px     | Labels, subtitles, body       |
| `base`        | 16px     | Primary text, navigation      |
| `lg`          | 18px     | Secondary section titles      |
| `2xl`         | 24px     | Primary section titles        |
| `normal`      | 400      | Body, descriptions            |
| `medium`      | 500      | Labels, navigation items      |
| `semibold`    | 600      | Titles, headers               |
| `bold`        | 700      | Primary titles                |

---

## 2. COLORS

### Light mode

| Token           | Value   | Usage                          |
| --------------- | ------- | ------------------------------ |
| `bg`            | #FFFFFF | Main background, topbar        |
| `bg-subtle`     | #F9FAFB | Topbar background, secondary areas |
| `bg-muted`      | #F3F4F6 | Statusbar, hover, alternation  |
| `bg-elevated`   | #FFFFFF | Drawer, modals                 |
| `text`          | #111827 | Primary text                   |
| `text-subtle`   | #6B7280 | Secondary text, subtitles      |
| `text-muted`    | #9CA3AF | Disabled text, statusbar       |
| `border`        | #E5E7EB | Standard borders               |
| `border-subtle` | #F3F4F6 | Discreet separators            |
| `border-strong` | #D1D5DB | Table headers                  |

### Dark mode

| Token           | Value   | Usage                  |
| --------------- | ------- | ---------------------- |
| `bg`            | #111827 | Main background, topbar |
| `bg-subtle`     | #1F2937 | Secondary areas        |
| `bg-muted`      | #1F2937 | Statusbar, hover       |
| `bg-elevated`   | #374151 | Drawer, modals         |
| `text`          | #F9FAFB | Primary text           |
| `text-subtle`   | #9CA3AF | Secondary text         |
| `text-muted`    | #6B7280 | Disabled text          |
| `border`        | #374151 | Standard borders       |
| `border-subtle` | #1F2937 | Discreet separators    |
| `border-strong` | #4B5563 | Table headers          |

### Primary color — Slate Blue

| Token         | Light   | Dark    |
| ------------- | ------- | ------- |
| `primary-50`  | #EEF2FF | —       |
| `primary-400` | —       | #818CF8 |
| `primary-600` | #4F46E5 | —       |
| `primary-900` | —       | #312E81 |

> Modification: replacing these 4 values is enough to change the primary color across the whole application.

### Semantic colors

| Token         | Light   | Dark    | Usage                  |
| ------------- | ------- | ------- | ---------------------- |
| `success-50`  | #F0FDF4 | —       | Success toast bg       |
| `success-600` | #16A34A | #4ADE80 | Success border, icon   |
| `warning-50`  | #FFFBEB | —       | Warning toast bg       |
| `warning-600` | #D97706 | #FCD34D | Warning border, icon   |
| `danger-50`   | #FFF1F2 | —       | Danger toast bg        |
| `danger-600`  | #DC2626 | #F87171 | Danger border, icon    |
| `info-50`     | #EFF6FF | —       | Info toast bg          |
| `info-600`    | #2563EB | #60A5FA | Info border, icon      |

### Charts / visualization palette

| Token           | Value         |
| --------------- | ------------- |
| `chart-primary` | `primary-600` |
| `chart-success` | `success-600` |
| `chart-warning` | `warning-600` |
| `chart-danger`  | `danger-600`  |
| `chart-info`    | `info-600`    |

---

## 3. SPACING

| Token       | Value | Usage                     |
| ----------- | ----- | ------------------------- |
| `spacing-1` | 4px   | Micro-spacing             |
| `spacing-2` | 8px   | Compact inner padding     |
| `spacing-3` | 12px  | Standard padding          |
| `spacing-4` | 16px  | Inter-element spacing     |
| `spacing-6` | 24px  | Main content padding      |
| `spacing-8` | 32px  | Major separation          |

---

## 4. COMPONENT SIZES

### Fixed sizes (global visual anchors)

| Token              | Value  | Usage                      |
| ------------------ | ------ | -------------------------- |
| `topbar-height`    | 48px   | Topbar height              |
| `statusbar-height` | 28px   | Statusbar height           |
| `drawer-width`     | 320px  | Right drawer width         |
| `content-xl`       | 1024px | Max centered content width |
| `icon-sm`          | 16px   | Small icon                 |
| `icon-md`          | 20px   | Standard icon              |
| `icon-lg`          | 24px   | Navigation / topbar icon   |

### Dynamic sizes — general principle

**Rule**: no component has a fixed height or width except the documented exceptions above. Dimensions result from content + padding.

| Component         | Width                                      | Height                     | Exception                                     |
| ----------------- | ------------------------------------------ | -------------------------- | --------------------------------------------- |
| Button            | content + horizontal padding               | content + vertical padding | aligned group: unified on the widest          |
| Input field       | stretches in its container (`setSizePolicy`) | content + vertical padding | —                                           |
| Table column      | content (`resizeColumnsToContents`)        | —                          | actions column: fixed                         |
| Topbar tab        | label + horizontal padding                 | `topbar-height`            | —                                             |
| Label             | content, wrap if constrained               | content                    | —                                             |
| Dropdown menu     | longest item                               | content                    | —                                             |
| Dialog / modal    | content                                    | content                    | min-width advised per context                 |
| QTreeView item    | content + indentation                      | vertical padding           | —                                             |
| Toast             | —                                          | multi-line content         | fixed width 320px                             |

---

## 5. SHAPE & SHADOWS

| Token    | Value                       |
| -------- | --------------------------- |
| `radius` | 0px — strict flat design    |
| `shadow` | none — strict flat design   |

---

## 6. TRANSITIONS

| Token                | Value      | Usage                   |
| -------------------- | ---------- | ----------------------- |
| `transition-default` | 150ms ease | hover, focus states     |
| `transition-slow`    | 250ms ease | Panels, drawer, tabs     |

---

## 7. FOCUS

| Token        | Value                               |
| ------------ | ----------------------------------- |
| `focus-ring` | 2px solid `primary-600`, offset 2px |

---

## 8. INTERACTIVE COMPONENT STATES

Applies to all buttons, tabs, clickable items:

| State                  | Rule                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `default`              | Base style defined by the component                                                               |
| `hover`                | `bg-muted` background, `transition-default` transition                                            |
| `active` / selected    | `primary-50` bg, `primary-600` text (light) / `primary-900` bg, `primary-400` text (dark)         |
| `disabled`             | 40% opacity, non-interactive                                                                      |
| `focus`                | `focus-ring` visible                                                                              |

---

## 9. BUTTONS

| Variant    | Background    | Text          | Border       |
| ---------- | ------------- | ------------- | ------------ |
| Primary    | `primary-600` | #FFFFFF       | none         |
| Secondary  | transparent   | `text`        | 1px `border` |
| Danger     | `danger-600`  | #FFFFFF       | none         |
| Ghost      | transparent   | `text-subtle` | none         |

**Dynamic sizing** — the size results from content + padding:

| Size          | Vertical padding   | Horizontal padding | Font                   |
| ------------- | ------------------ | ------------------ | ---------------------- |
| `sm`          | `spacing-1` (4px)  | `spacing-3` (12px) | `medium` `xs` (12px)   |
| `md` (default)| `spacing-2` (8px)  | `spacing-4` (16px) | `medium` `sm` (14px)   |
| `lg`          | `spacing-3` (12px) | `spacing-6` (24px) | `medium` `base` (16px) |

**Aligned button group**: width unified on the widest button (`setMinimumWidth` on all).

---

## 10. ICONS — qtawesome

Library: `qtawesome` (Font Awesome wrapper).
Icons are Python widgets colored dynamically — they do NOT go through QSS.

**Rule**: all icon colors are defined in `config.py`, never hardcoded in views or controllers.

```python
# config.py — example
ICON_COLORS = {
    "light": {
        "default":  "#6B7280",   # text-subtle
        "active":   "#4F46E5",   # primary-600
        "danger":   "#DC2626",   # danger-600
        "success":  "#16A34A",   # success-600
        "muted":    "#9CA3AF",   # text-muted
    },
    "dark": {
        "default":  "#9CA3AF",   # text-subtle
        "active":   "#818CF8",   # primary-400
        "danger":   "#F87171",   # danger-600
        "success":  "#4ADE80",   # success-600
        "muted":    "#6B7280",   # text-muted
    }
}
```

**Sizes**: use the tokens `icon-sm` (16px), `icon-md` (20px), `icon-lg` (24px).

```python
# Usage in a view
import qtawesome as qta
icon = qta.icon("fa6s.house", color=ICON_COLORS[theme]["default"], scale_factor=1.0)
```

**Theme change**: icons are recreated on theme toggle — no dynamic color update on an existing instance.

---

## 11. QSS APPLICATION RULES

1. **Zero hardcoded visual value in Python code.** Every color, size, font is in `styles_light.qss` / `styles_dark.qss`.
2. **Every styled widget has an `objectName`** matching a named QSS rule.
3. **Dark mode is handled by complete sheet replacement** (`styles_light.qss` → `styles_dark.qss`), not by partial override.
4. **Every QSS value is traced to a token in this file.** A `/* token : [name] */` comment indicates the source token.

```qss
/* Example — token : bg / text */
QMainWindow {
    background-color: #FFFFFF;
    color: #111827;
}
```
