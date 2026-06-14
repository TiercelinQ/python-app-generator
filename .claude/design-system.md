# Design System — v1.2

> Binding reference for all Python/PyQt6 applications.
> Use: Windows desktop applications, personal and professional use.
> Inseparable from `layout.md`.

## Changelog

| Version | Date       | Main change                                                                                  |
| ------- | ---------- | ------------------------------------------------------------------------------------------- |
| v1.2    | 2026-06-14 | line-height · dark semantic backgrounds · primary/danger hover-pressed stops · WCAG AA target · layering scale · dark surface ramp fix · dark charts · focus dark · selection · opacity/border-width tokens |
| v1.1    | 2026-06-12 | Dark mode tokens · semantic palette                                                          |
| v1.0    | initial    | Typography, colors, spacing, components, states                                              |

> The `primary-*` HSL derivation rule (compute the derived stops from the user-provided `primary-600`) lives in `rules/config.md`. Versions are tracked per file: QSS rules in `rules/qss.md`, layout in `layout.md`.

Every generated application references the active version in its `README.md`.

---

## 1. TYPOGRAPHY

| Token         | Value                          | Usage                         |
| ------------- | ------------------------------ | ----------------------------- |
| `font-family` | `"Segoe UI", system-ui, sans-serif` | All applications         |
| `xs`          | 12px                           | Statusbar, secondary labels   |
| `sm`          | 14px                           | Labels, subtitles, body       |
| `base`        | 16px                           | Primary text, navigation      |
| `lg`          | 18px                           | Secondary section titles      |
| `2xl`         | 24px                           | Primary section titles        |
| `normal`      | 400                            | Body, descriptions            |
| `medium`      | 500                            | Labels, navigation items      |
| `semibold`    | 600                            | Titles, headers               |
| `bold`        | 700                            | Primary titles                |

> Scale note: the step from `lg` (18px) to `2xl` (24px) is wider than the lower steps. No `xl` (20px) token is defined because no current usage needs it; do not add one speculatively.

### Line-height

| Token            | Value | Usage                          |
| ---------------- | ----- | ------------------------------ |
| `leading-tight`  | 1.25  | Titles (`lg`, `2xl`)           |
| `leading-normal` | 1.5   | Body, labels (`xs`, `sm`, `base`) |

> Qt constraint: QSS does not support a reliable `line-height` property. Apply leading via widget margins / `setContentsMargins`, or via `QTextDocument` / `QTextOption` for rich-text widgets. These tokens are the target ratios, not a QSS property.

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
| `bg-elevated`   | #1F2937 | Drawer, modals         |
| `bg-muted`      | #374151 | Statusbar, hover       |
| `text`          | #F9FAFB | Primary text           |
| `text-subtle`   | #9CA3AF | Secondary text         |
| `text-muted`    | #6B7280 | Disabled text          |
| `border`        | #374151 | Standard borders       |
| `border-subtle` | #1F2937 | Discreet separators    |
| `border-strong` | #4B5563 | Table headers          |

> Dark surface ramp: `bg` #111827 < {`bg-subtle`, `bg-elevated`} #1F2937 < `bg-muted` #374151. `bg-muted` is the lightest so that hover stays visible on every surface, including inside drawers and modals.

### Primary color — Slate Blue

| Token         | Light   | Dark    | Usage                              |
| ------------- | ------- | ------- | ---------------------------------- |
| `primary-50`  | #EEF2FF | —       | Selection / active bg (light)      |
| `primary-400` | —       | #818CF8 | Active text/border (dark)          |
| `primary-600` | #4F46E5 | —       | Active text/border, primary button bg (light) |
| `primary-700` | #4338CA | #4338CA | Primary button hover (both modes)  |
| `primary-800` | #3730A3 | #3730A3 | Primary button pressed (both modes) |
| `primary-900` | —       | #312E81 | Selection / active bg (dark)       |

> Modification: replacing `primary-50/400/600/700/800/900` is enough to change the primary color across the whole application. `primary-700` and `primary-800` are derived from `primary-600` by the same HSL rule (see `rules/config.md`); `primary-700`/`primary-800` share one value across modes (button hover/pressed).

### Semantic colors

| Token         | Light   | Dark    | Usage                       |
| ------------- | ------- | ------- | --------------------------- |
| `success-50`  | #F0FDF4 | #14532D | Success toast bg            |
| `success-600` | #16A34A | #4ADE80 | Success border, icon        |
| `warning-50`  | #FFFBEB | #78350F | Warning toast bg            |
| `warning-600` | #D97706 | #FCD34D | Warning border, icon        |
| `danger-50`   | #FFF1F2 | #7F1D1D | Danger toast bg             |
| `danger-600`  | #DC2626 | #F87171 | Danger border, icon         |
| `danger-700`  | #B91C1C | #B91C1C | Danger button hover         |
| `danger-800`  | #991B1B | #991B1B | Danger button pressed       |
| `info-50`     | #EFF6FF | #1E3A8A | Info toast bg               |
| `info-600`    | #2563EB | #60A5FA | Info border, icon           |

> Naming note: the `*-50` token is a **role** ("semantic surface / toast background"), not a fixed luminance level. Light = pale tint, Dark = deep tint of the same hue, so toasts stay readable in both themes (message text uses `text`, border/icon use `*-600`). On a `*-50` dark background the `text` color (#F9FAFB) and the `*-600` dark accent both keep WCAG AA contrast.

### Charts / visualization palette

| Token           | Light (value)         | Dark (value)          |
| --------------- | --------------------- | --------------------- |
| `chart-primary` | `primary-600` #4F46E5 | `primary-400` #818CF8 |
| `chart-success` | `success-600` #16A34A | #4ADE80               |
| `chart-warning` | `warning-600` #D97706 | #FCD34D               |
| `chart-danger`  | `danger-600` #DC2626  | #F87171               |
| `chart-info`    | `info-600` #2563EB    | #60A5FA               |

> Charts use the `-600` accents on a light background and the brighter dark accents (`primary-400` / `*-600` dark) on a dark background, for legible series against either theme.

### Text selection

| Token              | Light       | Dark        | Usage                         |
| ------------------ | ----------- | ----------- | ----------------------------- |
| `selection-bg`     | `primary-50` #EEF2FF | `primary-900` #312E81 | Selected text background |
| `selection-text`   | `text` #111827       | `text` #F9FAFB        | Selected text color      |

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
| Dialog / modal    | content                                    | content                    | min-width 480px (see `layout.md` §8)          |
| QTreeView item    | content + indentation                      | vertical padding           | —                                             |
| Toast             | —                                          | multi-line content         | fixed width 320px                             |

---

## 5. SHAPE, SHADOWS, BORDERS, OPACITY

| Token    | Value                     |
| -------- | ------------------------- |
| `radius` | 0px, strict flat design   |
| `shadow` | none, strict flat design  |

### Border widths

| Token                   | Value | Usage                                          |
| ----------------------- | ----- | ---------------------------------------------- |
| `border-width`          | 1px   | Standard borders, separators                   |
| `border-width-emphasis` | 2px   | Focus, active tab underline, field-in-error    |
| `border-width-accent`   | 4px   | Toast left accent                              |

### Opacity

| Token              | Value | Usage                                  |
| ------------------ | ----- | -------------------------------------- |
| `opacity-disabled` | 40%   | Disabled interactive elements          |
| `opacity-overlay`  | 40%   | Modal / drawer overlay (`text` color)  |

---

## 6. TRANSITIONS

| Token                | Value      | Usage                   |
| -------------------- | ---------- | ----------------------- |
| `transition-default` | 150ms ease | hover, focus states     |
| `transition-slow`    | 250ms ease | Panels, drawer, tabs     |

---

## 7. FOCUS

| Token        | Light                  | Dark                   |
| ------------ | ---------------------- | ---------------------- |
| `focus-ring` | 2px solid `primary-600` | 2px solid `primary-400` |

> Qt implementation: `outline-offset` is not reliable in QSS. Reserve the ring space with a 2px transparent border in the default state and swap it to the focus color on `:focus`, so the focus indicator appears without shifting the layout. The "offset" is conceptual, not a QSS property. See `rules/qss.md`.

---

## 8. INTERACTIVE COMPONENT STATES

Applies to **transparent-background interactive elements**: tabs, list/table/tree items, pagination buttons, Secondary and Ghost buttons. Colored-background buttons (Primary, Danger) follow their own hover/pressed rules in §9, because turning their background gray on hover would drop the semantic color.

| State                  | Rule                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `default`              | Base style defined by the component                                                               |
| `hover`                | `bg-muted` background, `transition-default` transition                                            |
| `pressed`              | `bg-muted` background (same as hover for neutral elements)                                        |
| `selected`             | `primary-50` bg, `primary-600` text (light) / `primary-900` bg, `primary-400` text (dark)         |
| `disabled`             | `opacity-disabled` (40%), non-interactive                                                         |
| `focus`                | `focus-ring` visible                                                                              |

> `selected` (a persistent chosen state: active tab, selected row) is distinct from `pressed` (transient mouse-down). Do not conflate them.

---

## 9. BUTTONS

| Variant    | Background    | Text          | Border       |
| ---------- | ------------- | ------------- | ------------ |
| Primary    | `primary-600` | #FFFFFF       | none         |
| Secondary  | transparent   | `text`        | 1px `border` |
| Danger     | `danger-600`  | #FFFFFF       | none         |
| Ghost      | transparent   | `text-subtle` | none         |

**States per variant** (transition `transition-default`):

| Variant    | hover         | pressed       | disabled              |
| ---------- | ------------- | ------------- | --------------------- |
| Primary    | `primary-700` | `primary-800` | `opacity-disabled` 40% |
| Danger     | `danger-700`  | `danger-800`  | `opacity-disabled` 40% |
| Secondary  | `bg-muted` bg | `bg-muted` bg | `opacity-disabled` 40% |
| Ghost      | `bg-muted` bg | `bg-muted` bg | `opacity-disabled` 40% |

> Colored buttons (Primary, Danger) darken on hover/pressed via their own `-700`/`-800` stops, never the neutral `bg-muted` rule of §8. `focus` shows the `focus-ring` on every variant.

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
        "success":  "#16A34A",   # success-600
        "warning":  "#D97706",   # warning-600
        "danger":   "#DC2626",   # danger-600
        "info":     "#2563EB",   # info-600
        "muted":    "#9CA3AF",   # text-muted
    },
    "dark": {
        "default":  "#9CA3AF",   # text-subtle
        "active":   "#818CF8",   # primary-400
        "success":  "#4ADE80",   # success-600 dark
        "warning":  "#FCD34D",   # warning-600 dark
        "danger":   "#F87171",   # danger-600 dark
        "info":     "#60A5FA",   # info-600 dark
        "muted":    "#6B7280",   # text-muted dark
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

---

## 12. ACCESSIBILITY

Target: **WCAG 2.1 level AA**.

| Criterion              | Rule                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Text contrast          | ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥ 18px bold or ≥ 24px) and UI components        |
| `text-muted` usage     | Disabled / decorative only — exempt from AA. Never for primary content                         |
| Statusbar text         | `text-subtle` (not `text-muted`). Reaches ~4.4:1 on `bg-muted`, marginal — essential/error status must use `text` |
| Minimum target size    | 24px. Button `sm` (~24px) is the floor; prefer `md` for touch-capable contexts                |
| Focus visibility       | `focus-ring` always visible on keyboard focus (§7), never removed                              |
| Reduced motion         | Respect the OS "show animations" setting; when off, disable `transition-default` / `transition-slow` |

> Contrast figures are computed estimates, not tool-measured. Re-check with a contrast checker before shipping a new primary color.

---

## 13. LAYERING (stacking order)

Logical z-order from back to front. A persistent `danger` toast must never be hidden, so toasts sit above modals.

| Layer            | Order | Element                          |
| ---------------- | ----- | -------------------------------- |
| `z-content`      | 0     | Main content                     |
| `z-drawer-overlay` | 100 | Drawer dimming overlay           |
| `z-drawer`       | 110   | Right drawer                     |
| `z-modal-overlay`| 200   | Modal dimming overlay            |
| `z-modal`        | 210   | Modal / dialog                   |
| `z-dropdown`     | 300   | Dropdown / context menu          |
| `z-toast`        | 400   | Toasts (always on top)           |

> Qt implementation: QSS has no `z-index`. Order is enforced with `raise()` / `stackUnder()` on sibling widgets, or by using top-level windows for modals and the toast layer. The numbers above are the canonical ordering, not a QSS property.
