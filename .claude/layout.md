# Layout System — v2.2

> Binding reference for all Python/PyQt6 applications.
> Built on `design-system.md v1.3`. The two files are inseparable.

## Changelog

| Version | Date       | Main change                                                                       |
| ------- | ---------- | --------------------------------------------------------------------------------- |
| v2.2    | 2026-06-14 | statusbar text `text-subtle` (WCAG) · dark toast tints · layering reference        |
| v2.1    | 2026-06-12 | 6 toast positions specified · neutral tabs · preferences clarified                 |
| v2.0    | initial    | Global structure, topbar, drawer, statusbar, recurring components                  |

Every generated application references the active version in its `README.md`.

---

## 1. GLOBAL STRUCTURE

```
┌─────────────────────────────────────────────────────┐
│              TOPBAR (48px)                          │
│  [ Logo / Name ]  [ Nav tabs ]  [ Theme ]          │
├─────────────────────────────────────────────────────┤
│                                                     │
│            MAIN CONTENT                             │
│            (scrollable area)                        │
│                                                     │
├─────────────────────────────────────────────────────┤
│                STATUSBAR (28px)                     │
└─────────────────────────────────────────────────────┘
```

**Right drawer** (optional, over the content):

```
┌─────────────────────────────────────────────────────┐
│                     TOPBAR                          │
├───────────────────────────────┬─────────────────────┤
│                               │                     │
│       MAIN CONTENT            │  DRAWER (320px)     │
│       (reduced)               │  sliding            │
│                               │                     │
├───────────────────────────────┴─────────────────────┤
│                   STATUSBAR                         │
└─────────────────────────────────────────────────────┘
```

**Toast** (overlaid, top-right corner):

```
┌─────────────────────────────────────────────────────┐
│                     TOPBAR              [ Toast 1 ] │
├─────────────────────────────────────────[ Toast 2 ]─┤
│                                                     │
│            MAIN CONTENT                             │
│                                                     │
├─────────────────────────────────────────────────────┤
│                   STATUSBAR                         │
└─────────────────────────────────────────────────────┘
```

---

## 2. WINDOW

| Token               | Value                        |
| ------------------- | ---------------------------- |
| `min-width`         | 1024px                       |
| `min-height`        | 768px                        |
| state on launch     | restored (position + size)   |
| theme on launch     | follows the OS theme         |
| OS default theme    | light                        |

---

## 3. TOPBAR

| Token              | Value                  |
| ------------------ | ---------------------- |
| height             | `topbar-height` = 48px |
| light mode bg      | `bg` = #FFFFFF         |
| dark mode bg       | `bg` = #1A1A1F         |
| bottom border      | 1px `border`           |
| horizontal padding | `spacing-4` = 16px     |

### Topbar zones (left → right)

```
[ Logo / App name ]  [ Navigation tabs ]  ···  [ Theme ]
```

| Zone                              | Content                         | Width       |
| --------------------------------- | ------------------------------- | ----------- |
| Left                              | SVG logo 24px + app name        | fixed       |
| Left or Center (Phase 3 choice)   | Navigation tabs (QTabBar)       | flexible    |
| Right                             | Light/dark theme selector       | fixed — 40px |

Tab alignment (left-after-logo OR centered) is decided in Phase 3.

### Logo / App name

- SVG icon `icon-lg` (24px) + label `semibold` `base` (16px).
- Color: `text`.
- Not clickable.

### Navigation tabs (QTabBar)

- Embedded in the topbar, alignment defined in Phase 3 (left-after-logo or centered).
- Maximum 5 visible tabs. Beyond → `···` dropdown menu.
- Active tab: `primary-600` text (light) / `primary-400` (dark), 2px `primary-600` / `primary-400` bottom border.
- Inactive tab: `text-subtle` text, transparent background.
- Hover: `bg-muted` background, `transition-default` transition.
- Font: `medium` `sm` (14px).
- Tab height: `topbar-height` = 48px (full topbar height).
- Horizontal padding per tab: `spacing-4` = 16px.

### Theme selector

- Icon only (sun / moon), size `icon-lg` = 24px.
- Mandatory tooltip: "Passer en mode sombre" / "Passer en mode clair".
- Instant toggle — persisted in user preferences.

---

## 4. MAIN CONTENT AREA

| Token               | Value                          |
| ------------------- | ------------------------------ |
| light mode bg       | `bg` = #FFFFFF                 |
| dark mode bg        | `bg` = #1A1A1F                 |
| inner padding       | `spacing-6` = 24px             |
| scroll              | vertical — `QScrollArea`       |
| max content width   | `content-xl` = 1024px (centered) |

### Section header

```
[ Section title ]   [ Subtitle / short description ]
```

- Title: `bold` `2xl` (24px), color `text`.
- Subtitle: `normal` `sm` (14px), color `text-subtle`.
- Bottom margin: `spacing-6` = 24px before the content.

---

## 5. TOAST

Fully replaces the inline banner. No inline banner in the applications.

### Position — Phase 3 choice

6 positions available. Default: `top-right`.

| Position       | Anchor              | Enter animation                | Exit animation                  |
| -------------- | ------------------- | ------------------------------ | ------------------------------- |
| `top-right`    | top + right         | Slide from the right           | Fade + slide right              |
| `top-left`     | top + left          | Slide from the left            | Fade + slide left               |
| `top-center`   | top + center        | Slide from the top             | Fade + slide up                 |
| `bottom-right` | bottom + right      | Slide from the right           | Fade + slide right              |
| `bottom-left`  | bottom + left       | Slide from the left            | Fade + slide left               |
| `bottom-center`| bottom + center     | Slide from the bottom          | Fade + slide down               |

### Margins and stacking

| Token                            | Value                                                  |
| -------------------------------- | ------------------------------------------------------ |
| width                            | 320px (fixed)                                          |
| margin from edge                 | `spacing-4` = 16px                                     |
| margin from topbar / statusbar   | `spacing-4` = 16px (per top/bottom anchor)             |
| spacing between toasts           | `spacing-2` = 8px                                      |
| stacking                         | Vertical, queue, no overlap                            |
| stacking direction (top)         | new toast on top, older ones descend                   |
| stacking direction (bottom)      | new toast at bottom, older ones rise                   |
| transition duration              | `transition-slow` = 250ms                              |

### Implementation

- The `ToastManager` (`views/toast_manager.py`) receives the position from `config.TOAST_POSITION`.
- `config.TOAST_POSITION` = `"top-right"` by default, modified per Phase 3 choice.
- The manager computes the anchor from the main window's `geometry()`.

### Display durations

| Type      | Duration   | Manual dismiss      |
| --------- | ---------- | ------------------- |
| `success` | 4s         | No                  |
| `info`    | 4s         | No                  |
| `warning` | 6s         | Yes (×)             |
| `danger`  | persistent | Yes (×) mandatory   |

### Toast anatomy

```
┌────────────────────────────────────┐
│ [icon]  Main message           [×] │
│         Optional description       │
└────────────────────────────────────┘
```

| Token              | Value                                        |
| ------------------ | -------------------------------------------- |
| padding            | `spacing-3` vertical, `spacing-4` horizontal |
| left border        | 4px semantic color                           |
| bg                 | semantic bg (`*-50`)                         |
| message font       | `medium` `sm` (14px)                         |
| description font   | `normal` `xs` (12px), `text-subtle`          |
| icon               | `icon-md` = 20px                             |

| Type      | Bg           | Border        | Icon           |
| --------- | ------------ | ------------- | -------------- |
| `success` | `success-50` | `success-600` | check-circle   |
| `warning` | `warning-50` | `warning-600` | alert-triangle |
| `danger`  | `danger-50`  | `danger-600`  | x-circle       |
| `info`    | `info-50`    | `info-600`    | info           |

> `*-50` is the toast surface role: pale tint in light, deep tint in dark (see `design-system.md §2`). Both keep AA contrast with `text` and the `*-600` accent. Toast icons use the matching `ICON_COLORS` entry (`config.py`), per mode.
> Layering: toasts sit above modals (`z-toast` = 400, see `design-system.md §13`) so a persistent `danger` toast is never hidden.

---

## 6. RIGHT DRAWER

| Token            | Value                                                  |
| ---------------- | ------------------------------------------------------ |
| width            | `drawer-width` = 320px                                 |
| animation        | slide from the right, `transition-slow` = 250ms        |
| light mode bg    | `bg-elevated` = #FFFFFF                                |
| dark mode bg     | `bg-elevated` = #2A2A35                                |
| left border      | 1px `border`                                           |
| padding          | `spacing-6` = 24px                                     |
| overlay bg       | `text` 40% opacity                                     |

- Opened by explicit action only. Never automatically.
- Close: click overlay, Escape key, or × button in the drawer.
- Drawer header: `semibold` `lg` (18px) title + × button aligned right.
- Drawer content: vertically scrollable on overflow.

---

## 7. STATUSBAR

| Token              | Value                     |
| ------------------ | ------------------------- |
| height             | `statusbar-height` = 28px |
| light mode bg      | `bg-muted` = #F3F4F6      |
| dark mode bg       | `bg-muted` = #313140      |
| top border         | 1px `border`              |
| horizontal padding | `spacing-4` = 16px        |
| font               | `normal` `xs` (12px)      |
| text color         | `text-subtle`             |

> WCAG: `text-subtle` on `bg-muted` reaches ~4.4:1, marginal vs AA (4.5:1). Essential or error status must use `text` for full contrast. `text-muted` is reserved for disabled/decorative use (see `design-system.md §12`).

### Statusbar zones (left → right)

```
[ Status message ]  ···  [ Progress ]  [ Contextual info ]
```

| Zone   | Content                                                                   |
| ------ | ------------------------------------------------------------------------- |
| Left   | Current status message ("Prêt", "Chargement…", "3 éléments sélectionnés") |
| Center | Compact `QProgressBar` (8px) — visible only when an operation is running  |
| Right  | Fixed contextual info (record count, version, DB connection…)             |

---

## 8. RECURRING COMPONENTS

### Data table (QTableView)

- Header: `bg-subtle` bg, `semibold` `sm` (14px), `text-subtle`.
- Header bottom border: 2px `border-strong`.
- Row: dynamic height (vertical padding `spacing-2` = 8px), 1px `border-subtle` bottom border.
- Columns: dynamic width (`resizeColumnsToContents`). Exception: actions column — fixed width per content.
- Selected row: `primary-50` / `primary-900` (dark) bg.
- Row hover: `bg-muted` bg.
- Row alternation: disabled (flat design).
- Pagination below the table if > 50 rows.

### Input form

- Labels above the fields, `medium` `sm` (14px), `text`.
- Fields: stretched width in the container (`setSizePolicy(Expanding, Fixed)`), dynamic height (vertical padding `spacing-2` = 8px).
- Spacing between fields: `spacing-4` = 16px.
- Field in error: 2px `danger-600` border + `danger-600` message below the field, `xs` (12px).
- Form actions: aligned right — Cancel (secondary) + Confirm (primary), dynamic width per label.

### Tree view (QTreeView)

- Indentation per level: `spacing-4` = 16px.
- Expand/collapse icon: chevron, `icon-sm` = 16px, `text-muted`.
- Item height: dynamic (vertical padding `spacing-1` = 4px).
- Selected item: `primary-50` / `primary-900` (dark) bg.

### Charts / Visualization

- Background: transparent (inherits the main content).
- Palette: `chart-primary`, `chart-success`, `chart-warning`, `chart-danger`, `chart-info`.
- Legend: `normal` `sm` (14px), `text-subtle`.
- No shadow (flat design).

### Modal (QDialog)

```
┌─────────────────────────────────────┐
│  Modal title                    [×] │
├─────────────────────────────────────┤
│                                     │
│  Content (form, text…)              │
│                                     │
├─────────────────────────────────────┤
│              [ Cancel ] [ Confirm ] │
└─────────────────────────────────────┘
```

| Token            | Value                              |
| ---------------- | ---------------------------------- |
| width            | dynamic per content, min 480px     |
| light mode bg    | `bg` = #FFFFFF                     |
| dark mode bg     | `bg` = #1A1A1F                     |
| border           | 1px `border`                       |
| padding          | `spacing-6` = 24px                 |
| overlay bg       | `text` 40% opacity                 |

- Opened by explicit action only.
- Close: × button, Cancel, Escape key, or click overlay.
- Header: `semibold` `lg` (18px) title + × button aligned right, 1px `border-subtle` bottom border.
- Footer: actions aligned right — Cancel (secondary) + Confirm (primary), 1px `border-subtle` top border.
- Content: vertically scrollable on overflow.
- Zero native `QMessageBox` — use a styled `QDialog`.

### Pagination

Shown below a `QTableView` containing more than 50 rows.

```
[ ← ]  [ 1 ]  [ 2 ]  [ 3 ]  ···  [ 12 ]  [ → ]
                  Page 2 sur 12
```

| Token                   | Value                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| position                | below the table, aligned right                                                                    |
| spacing from table      | `spacing-4` = 16px                                                                                |
| page button             | dynamic per number, padding `spacing-2` horizontal                                                |
| active button           | `primary-50` bg, `primary-600` text (light) / `primary-900` bg, `primary-400` text (dark)         |
| inactive button         | transparent, `text-subtle` text                                                                   |
| button hover            | `bg-muted` bg                                                                                      |
| ← → buttons             | `icon-sm` (16px) icons, disabled on first/last page                                               |
| page label              | `normal` `xs` (12px), `text-muted`, centered below the buttons                                    |
| max visible pages       | 5 numbers — `···` ellipsis beyond                                                                 |

---

## 9. GLOBAL KEYBOARD NAVIGATION

| Shortcut            | Action                                 |
| ------------------- | -------------------------------------- |
| `Tab` / `Shift+Tab` | Navigate between interactive elements  |
| `Enter` / `Space`   | Activate focused button / item         |
| `Escape`            | Close active drawer / modal / dropdown |
| `Alt+1…9`           | Direct navigation to tab N             |
| `Ctrl+,`            | Open Settings                          |

---

## 10. PERSISTED PREFERENCES

`preferences.json` file at the project root (gitignored).
In `.exe` packaging mode: `%APPDATA%/[AppName]/preferences.json` (see `@rules/config.md`).

| Preference         | Default value     |
| ------------------ | ----------------- |
| theme              | OS system         |
| window size        | 1280×800          |
| window position    | centered          |
| drawer state       | closed            |
| language (if i18n) | fr                |
| toast position     | top-right         |

Read/write via `utils/helpers.py` — `load_preferences()` / `save_preferences(data)`.

---

## 11. DESIGN SYSTEM CROSS-REFERENCE

This file does not redefine tokens — it consumes them. Every visual value is traced to `design-system.md v1.3`.

| Need                       | Token                                          |
| -------------------------- | ---------------------------------------------- |
| Main background            | `bg`                                           |
| Secondary areas background | `bg-subtle`                                    |
| Drawer background          | `bg-elevated`                                  |
| Primary text               | `text`                                         |
| Secondary text             | `text-subtle`                                  |
| Borders                    | `border` / `border-subtle` / `border-strong`   |
| Active / selection color   | `primary-600` (light) / `primary-400` (dark)   |
| Focus                      | `focus-ring` 2px offset 2px                    |
| Panel transitions          | `transition-slow` = 250ms                      |
| State transitions          | `transition-default` = 150ms                   |
| Shape                      | `radius` = 0px (flat design)                   |
| Shadows                    | none (flat design)                             |
| Line-height                | `leading-tight` 1.25 / `leading-normal` 1.5    |
| Overlay opacity            | `opacity-overlay` 40% (`text` color)           |
| Stacking order             | layering scale (`design-system.md §13`)        |
```
