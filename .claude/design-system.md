# Design System — v2.0

> Binding reference for all Python/PySide6 applications.
> Use: Windows desktop applications, personal and professional use.
> Inseparable from `layout.md`.

**Visual language (v2.0)**: depth is expressed by the **stroke** (borders), never by shadows or elevation. Corners are softly rounded (5px). Neutrals carry a low tint of the project accent, so every generated application has its own atmosphere. Motion is discreet (asymmetric deceleration, `QPropertyAnimation` only) with **one** signature gesture: the sliding underline on tabs and horizontal navigation.

## Changelog

| Version | Date       | Main change                                                                                  |
| ------- | ---------- | ------------------------------------------------------------------------------------------- |
| v2.0    | 2026-07-16 | modernization: `radius` 0 → **5px** · typography → **system font** (QApplication default, no pinned family) · **accent-tinted neutrals** (all neutral roles derived from the accent hue; explicit palette roles still win) · **semantic colors derived per project** (fixed hue anchors, harmonized ±6° toward the accent; info = accent) · hover on neutral elements = **border strengthening** (replaces `bg-muted` fill) · easing `ease-out` (decelerate, `QEasingCurve.OutCubic`) 160/240ms via `config.ANIM_*` · **signature gesture**: sliding underline (tabs / horizontal nav, `QPropertyAnimation`) · icons qtawesome/Font Awesome → **Lucide** (vendored SVGs, stroke 1.75, `utils/icons.py` helper) · floating layers marked by `border-strong` (shadows still forbidden) |
| v1.6    | 2026-06-27 | default accent → **Steel Blue** `#4682B4` (chromatic in both themes, derived like the named palettes) · dark **surfaces** stay neutral grey · `onPrimary` stays a single white value (white on `#4682B4` 4.1:1) · Teal kept as a named palette |
| v1.5    | 2026-06-20 | default accent → **Teal** `#0D9488` · dark surfaces stay neutral grey · grey-accent dark special-case removed |
| v1.4    | 2026-06-19 | full **palette** model (5 roles/theme) · named palette catalog + custom palette · WCAG AA check (warn) |
| v1.3    | 2026-06-14 | dark theme re-skin: 4-step dark surface ramp · Steel Blue primary (both modes)               |
| v1.2    | 2026-06-14 | line-height · dark semantic backgrounds · WCAG AA target · layering scale                    |
| v1.1    | 2026-06-12 | Dark mode tokens · semantic palette                                                          |
| v1.0    | initial    | Typography, colors, spacing, components, states                                              |

> Aligns with the Electron generator `design-system.md v2.0` and Flutter `v2.0` (shared palette + derivation model). The `primary-*` HSL derivation rule lives in `rules/config.md`. Versions are tracked per file: QSS rules in `rules/qss.md`, layout in `layout.md`.

Every generated application references the active version in its `README.md`.

---

## 1. TYPOGRAPHY

| Token         | Value                          | Usage                         |
| ------------- | ------------------------------ | ----------------------------- |
| `font-family` | system font (no pinned family) | All applications              |
| `xs`          | 12px                           | Statusbar, secondary labels   |
| `sm`          | 14px                           | Labels, subtitles, body       |
| `base`        | 16px                           | Primary text, navigation      |
| `lg`          | 18px                           | Secondary section titles      |
| `xl`          | 20px                           | Intermediate titles           |
| `2xl`         | 24px                           | Primary section titles        |
| `normal`      | 400                            | Body, descriptions            |
| `medium`      | 500                            | Labels, navigation items      |
| `semibold`    | 600                            | Titles, headers               |
| `bold`        | 700                            | Primary titles                |

> v2.0: do **not** set `font-family` in the QSS sheets. The `QApplication` default font is the native UI face of the host OS — the application always looks native, zero embedded font. QSS sets sizes and weights only. (Pinning "Segoe UI" would freeze the Windows 10 face.)

### Line-height

| Token            | Value | Usage                          |
| ---------------- | ----- | ------------------------------ |
| `leading-tight`  | 1.25  | Titles (`lg`, `2xl`)           |
| `leading-normal` | 1.5   | Body, labels (`xs`, `sm`, `base`) |

> Qt constraint: QSS does not support a reliable `line-height` property. Apply leading via widget margins / `setContentsMargins`, or via `QTextDocument` / `QTextOption` for rich-text widgets. These tokens are the target ratios, not a QSS property.

### Numerals

Tables, statusbar counters, and any column of figures align digits vertically: set a fixed-width numeral variant via `QFont.setStyleHint`/font features where the widget allows it, or right-align numeric columns (`QTableView` numeric delegates) so columns of figures stay readable.

---

## 2. COLORS

A project's colors come from a **palette**. In v2.0 only the **accent is mandatory**: every neutral role, the accent stops, and the semantic colors **derive** from it. The four other roles (main background, secondary background, text, details) remain available as **explicit overrides** — when provided, their values win over the derivation (same precedence rule as v1.6 presets).

Token placement (unchanged mechanics): the **neutrals and semantics** live as literal hex in `resources/styles_light.qss` / `resources/styles_dark.qss`; the **accent stops** (`PRIMARY_*`, `ON_PRIMARY`), `ICON_COLORS`, and — if the splash is on — `SPLASH_COLORS` live in `config.py` (`rules/config.md`).

### Palette roles → tokens

| Role (palette)      | Mandatory | Drives        | Also derives                                                                                  |
| ------------------- | --------- | ------------- | ---------------------------------------------------------------------------------------------- |
| Accent              | yes       | `primary-600` | `primary-50/400/700/800/900`, `primary`, `primary-bg`, `selection-bg`, `focus-ring`, `onPrimary`, `ICON_COLORS`, **all neutral tokens** (tinting rule below), **all semantic tokens** (harmonization rule below) |
| Main background     | optional  | `bg`          | `bg-elevated` (= `bg` in light)                                                                |
| Secondary background| optional  | `bg-subtle`   | `bg-muted` (`bg-subtle` darkened ~3 % L)                                                       |
| Text                | optional  | `text`        | `text-subtle` (mix text→bg ~45 %), `text-muted` (mix text→bg ~62 %)                            |
| Details             | optional  | `border`      | `border-subtle` (mix border→bg ~50 %), `border-strong` (mix border→text ~12 %)                 |

### Derivation rules (computed by Claude in Phase 1, written as literal hex)

**Accent stops** (unchanged from v1.6 — same H/S as the accent, lightness varies): `primary-50` L≈95 %, `primary-400` L≈70 %, `primary-700` L≈50 %, `primary-800` L≈42 %, `primary-900` L≈25 %. Usage tokens: `primary` = `primary-600` (light) / `primary-400` (dark); `primary-bg` = `primary-50` (light) / `primary-900` (dark). Method (`colorsys`): `rules/config.md`. `onPrimary` (button text on the accent) = `#FFFFFF` or near-black, whichever wins contrast on the accent.

**Tinted neutrals** (new in v2.0). Let **H** be the accent hue. Every neutral token is `hsl(H, S, L)` with the fixed S/L targets below. The tint is atmospheric, never saturated: S stays ≤ 33 % in light, ≤ 24 % in dark. When an optional palette role is provided, its explicit value replaces the tinted target for that token, and its supporting tokens derive from it by the mix rules of the role table above.

| Token           | Light `hsl(H, S%, L%)` | Dark `hsl(H, S%, L%)` |
| --------------- | ---------------------- | ---------------------- |
| `bg`            | 30, 99.4               | 14, 11                 |
| `bg-subtle`     | 25, 97                 | 16, 15                 |
| `bg-elevated`   | = `bg`                 | 15, 17                 |
| `bg-muted`      | 22, 94.5               | 16, 19                 |
| `text`          | 33, 9                  | 24, 96                 |
| `text-subtle`   | 10, 44                 | 13, 63                 |
| `text-muted`    | 12, 64                 | 11, 42                 |
| `border`        | 18, 90                 | 14, 23                 |
| `border-subtle` | 20, 94                 | 15, 18                 |
| `border-strong` | 14, 64                 | 15, 38                 |

> Dark surface ramp stays ascending: `bg` < `bg-subtle` < `bg-elevated` < `bg-muted`, so hover stays visible on every surface, including inside drawers and modals. Same rationale as v1.6.

### Default palette — Steel Blue accent `#4682B4` (H = 207), computed hex

Light (`styles_light.qss`):

| Token           | Value   | Token           | Value   |
| --------------- | ------- | --------------- | ------- |
| `bg`            | #FDFEFF | `text`          | #0F181E |
| `bg-subtle`     | #F5F8FA | `text-subtle`   | #65717B |
| `bg-muted`      | #EEF1F4 | `text-muted`    | #98A4AE |
| `bg-elevated`   | #FDFEFF | `border`        | #E1E6EA |
| —               | —       | `border-subtle` | #ECF0F3 |
| —               | —       | `border-strong` | #96A4B0 |

Dark (`styles_dark.qss`, derived):

| Token           | Value   | Token           | Value   |
| --------------- | ------- | --------------- | ------- |
| `bg`            | #181C20 | `text`          | #F2F5F7 |
| `bg-subtle`     | #20272C | `text-subtle`   | #94A2AD |
| `bg-elevated`   | #252C32 | `text-muted`    | #5F6C77 |
| `bg-muted`      | #293138 | `border`        | #323B43 |
| —               | —       | `border-subtle` | #272F35 |
| —               | —       | `border-strong` | #52626F |

> Hex values are computed from the HSL targets; re-check with a contrast tool before shipping (Phase 1 runs the AA check, §12).

### Named palettes (Phase 1 catalog)

`p1-scoping` presents these. In v2.0 a preset is defined by its **accent alone**; the four optional roles may still be listed to override the tint (e.g. Amber warms its backgrounds beyond the rule). Custom palettes: 1 mandatory hex (accent) + up to 4 optional overrides.

| Name                 | Accent  | Optional overrides                     |
| -------------------- | ------- | -------------------------------------- |
| Steel Blue (default) | #4682B4 | —                                      |
| Teal                 | #0D9488 | —                                      |
| Forest               | #059669 | —                                      |
| Slate                | #4F46E5 | —                                      |
| Amber                | #B45309 | Main bg #FFFDFB, Secondary bg #FBF6EF  |
| Ruby                 | #BE123C | —                                      |

### Accent — Steel Blue (default palette)

Unchanged mechanics from v1.6: a single chromatic ramp used in **both** themes; only the usage flips (`primary` = `primary-600` light / `primary-400` dark; `primary-bg` = `primary-50` light / `primary-900` dark). Replacing the `PRIMARY_*` stops in `config.py` (+ the derived neutrals/semantics in both sheets) is enough to change the accent across the whole application.

| Token         | Value   | Usage                                                         |
| ------------- | ------- | ------------------------------------------------------------- |
| `primary-50`  | #EDF3F8 | Selection / active bg (light)                                 |
| `primary-400` | #5A9FD4 | Active text/border (dark) — bright, reads on the dark `bg`    |
| `primary-600` | #4682B4 | Primary button fill (both themes); active text/border (light) |
| `primary-700` | #396A93 | Primary button hover                                          |
| `primary-800` | #2F5879 | Primary button pressed                                        |
| `primary-900` | #2A4F72 | Selection / active bg (dark)                                  |

> `onPrimary` (primary-button text): `#FFFFFF` in **both** themes for Steel Blue (white on `#4682B4` 4.1:1, AA UI/large; reported by the Phase 1 WCAG check). The dark foreground accent is the brighter `primary-400 #5A9FD4`, not the button fill.

### Semantic colors (derived — harmonized with the project atmosphere)

New in v2.0. Semantic colors keep **fixed hue anchors** so the meaning never drifts, but their exact hue/saturation/lightness are **derived per project** so they share the tinted atmosphere of the neutrals. **Info is the accent itself.**

**Derivation rule.** Let **Ha** be the accent hue and **Hs** the anchor hue of a semantic color. The harmonized hue is:

```
Hs' = Hs + clamp(shortest_angle(Ha − Hs), −10°, +10°) × 0.6      → shift capped at ±6°
```

| Semantic | Anchor Hs | Light `*-600` `hsl(Hs', S%, L%)` | Dark `*-600` `hsl(Hs', S%, L%)` |
| -------- | --------- | --------------------------------- | -------------------------------- |
| success  | 152       | S 48, L 38                        | S 42, L 60                       |
| warning  | 38        | S 62, L 40                        | S 56, L 60                       |
| danger   | 355       | S 52, L 48                        | S 46, L 62                       |
| info     | = accent  | `info-600` = `primary-600`        | `info-600` = `primary-400`       |

**Surface tokens** (`*-50`, toast backgrounds):
- Light: `*-50` = sRGB mix of `bg` 92 % + `*-600` 8 %.
- Dark: `*-50` = sRGB mix of `bg` 82 % + dark `*-600` 18 %.
- Info: `info-50` = `primary-bg` (`primary-50` light / `primary-900` dark).

> Naming note (kept from v1.6): the `*-50` token is a **role** ("semantic surface / toast background"), not a fixed luminance level. Light = pale tint, Dark = deep tint of the same hue, so toasts stay readable in both themes (message text uses `text`, border/icon use `*-600`).

**Danger button stops** (fill logic unchanged from v1.4/v1.6: red fill + white text in both themes):
- `danger-700` = light `danger-600` at L −7 %; `danger-800` at L −13 %.

Default palette (accent H 207) computed hex:

| Token         | Light   | Dark    | Usage                  |
| ------------- | ------- | ------- | ---------------------- |
| `success-50`  | #EFF6F3 | #26372F | Success toast bg       |
| `success-600` | #328F6D | #6EC4A4 | Success border, icon   |
| `warning-50`  | #F8F5EC | #392F1B | Warning toast bg       |
| `warning-600` | #A58327 | #D2B460 | Warning border, icon   |
| `danger-50`   | #F8EFF1 | #38222B | Danger toast bg        |
| `danger-600`  | #BA3B52 | #CB7282 | Danger border, icon    |
| `danger-700`  | #A23448 | #A23448 | Danger button hover    |
| `danger-800`  | #8A2C3D | #8A2C3D | Danger button pressed  |
| `info-50`     | = `primary-50` | = `primary-900` | Info toast bg |
| `info-600`    | = `primary-600` | = `primary-400` | Info border, icon |

> The ±6° cap keeps every semantic color instantly recognizable across projects (a danger is always red-family, a success always green-family). Every `*-600`/`*-50` pair must pass the §12 checks — Phase 1 verifies and reports.

### Charts / visualization palette

Unchanged mechanics — charts consume the derived accent and semantic values per theme, so series stay legible against either background.

| Token           | Light            | Dark             |
| --------------- | ---------------- | ---------------- |
| `chart-primary` | `primary-600`    | `primary-400`    |
| `chart-success` | `success-600`    | `success-600` dark |
| `chart-warning` | `warning-600`    | `warning-600` dark |
| `chart-danger`  | `danger-600`     | `danger-600` dark  |
| `chart-info`    | `info-600`       | `info-600` dark    |

### Text selection

| Token            | Light                 | Dark                   | Usage                    |
| ---------------- | --------------------- | ---------------------- | ------------------------ |
| `selection-bg`   | `primary-50`          | `primary-900`          | Selected text background |
| `selection-text` | `text`                | `text`                 | Selected text color      |

---

## 3. SPACING

Unchanged from v1.6.

| Token       | Value | Usage                     |
| ----------- | ----- | ------------------------- |
| `spacing-1` | 4px   | Micro-spacing             |
| `spacing-2` | 8px   | Compact inner padding     |
| `spacing-3` | 12px  | Standard padding          |
| `spacing-4` | 16px  | Inter-element spacing     |
| `spacing-5` | 20px  | Intermediate spacing      |
| `spacing-6` | 24px  | Main content padding      |
| `spacing-8` | 32px  | Major separation          |

---

## 4. COMPONENT SIZES

Unchanged from v1.6 (fixed anchors + dynamic sizing principle).

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

**The stroke is the language of depth.** An element detaches from the background by its border, never by a shadow. Hierarchy = border strength: `border-subtle` < `border` < `border-strong`. Floating layers (dropdown, modal, drawer) use `border-strong` — that is their elevation; the toast's stroke marker is its 4px semantic left accent (`layout.md §5`).

| Token    | Value                                              |
| -------- | -------------------------------------------------- |
| `radius` | 5px, uniform                                       |
| `shadow` | none — `QGraphicsDropShadowEffect` forbidden       |

> `radius` applies to every rounded element: buttons, fields, cards, toasts, modals, badges (`border-radius: 5px` in QSS). Nested radius (e.g. menu items inside a 5px menu): 3px (`radius` − 2). Shadows remain forbidden as in v1.6, in QSS and in code.

### Border widths

| Token                   | Value | Usage                                          |
| ----------------------- | ----- | ---------------------------------------------- |
| `border-width`          | 1px   | Standard borders, separators                   |
| `border-width-emphasis` | 2px   | Focus, signature underline, field-in-error     |
| `border-width-accent`   | 4px   | Toast left accent                              |

### Opacity

| Token              | Value | Usage                                  |
| ------------------ | ----- | -------------------------------------- |
| `opacity-disabled` | 40%   | Disabled interactive elements          |
| `opacity-overlay`  | 40%   | Modal / drawer overlay (`text` color)  |

---

## 6. TRANSITIONS

New in v2.0: a single asymmetric easing (fast start, soft landing). QSS cannot animate — state changes (hover, focus) apply **instantly**, which is accepted; animation exists only where Qt code drives it (`QPropertyAnimation`).

| Token / constant     | Value                                         | Usage                                      |
| -------------------- | --------------------------------------------- | ------------------------------------------ |
| `ease-out`           | `QEasingCurve.Type.OutCubic`                  | Every animation                            |
| `ANIM_DEFAULT_MS`    | 160 (`config.py`)                             | Reserved for short functional animations   |
| `ANIM_SLOW_MS`       | 240 (`config.py`)                             | Drawer slide, signature underline          |

**Motion policy**: the **drawer slide** (functional panel movement) and the **signature underline** (§8) are the only animated visuals. No entry animations on dropdowns, modals, or toasts; QSS state changes stay instant. The underline is the only *expressive* movement in the system.

---

## 7. FOCUS

Unchanged from v1.6.

| Token        | Light                   | Dark                    |
| ------------ | ----------------------- | ----------------------- |
| `focus-ring` | 2px solid `primary-600` | 2px solid `primary-400` |

> Qt implementation: `outline-offset` is not reliable in QSS. Reserve the ring space with a transparent border in the default state and swap it to the focus color on `:focus`, compensating padding so the layout does not shift. The "offset" is conceptual, not a QSS property. See `rules/qss.md`.

---

## 8. INTERACTIVE COMPONENT STATES

Applies to **neutral interactive elements**: tabs, list/table/tree items, pagination buttons, Secondary and Ghost buttons. Colored-background buttons (Primary, Danger) follow §9.

**v2.0 change — hover is a stroke event, not a fill event.** The `bg-muted` hover fill of v1.6 is replaced by border strengthening: on hover, the element's border climbs one step. Elements without a visible border always carry a **transparent 1px border** in QSS so hover never shifts layout.

| State      | Rule                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------- |
| `default`  | Base style; borderless items have `border: 1px solid transparent`                                  |
| `hover`    | Border climbs one step: transparent → `border`; `border` → `border-strong` (instant — QSS cannot transition). Wide list/table rows may add `bg-subtle` as a secondary cue |
| `pressed`  | `bg-muted` background (transient press feedback)                                                   |
| `selected` | `primary-bg` background, `primary` text (`primary-50`/`primary-600` light, `primary-900`/`primary-400` dark). Tabs / horizontal nav instead use the **signature underline** (below) |
| `disabled` | `opacity-disabled` (40%), non-interactive                                                          |
| `focus`    | `focus-ring` visible                                                                               |

> `selected` (persistent) remains distinct from `pressed` (transient mouse-down). Do not conflate them.

### Signature gesture — the sliding underline

The selected indicator of **tabs and horizontal navigation** is a 2px accent underline that **slides** from the previous item to the new one (240ms, `OutCubic`). It is the identity gesture of the system: implement it wherever a horizontal selection exists, and nowhere else.

Reference implementation — a dedicated widget `views/sliding_underline.py` (PySide6 only, no business logic):

```python
"""Signature underline — the only expressive animated visual (design-system §6/§8)."""

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtWidgets import QWidget

import config

_HEIGHT = 2  # token: border-width-emphasis


class SlidingUnderline(QWidget):
    """2px accent bar overlaid on the tab row; slides to the active tab."""

    def __init__(self, parent: QWidget, theme: str) -> None:
        super().__init__(parent)
        self.setFixedHeight(_HEIGHT)
        self.apply_theme(theme)
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(config.ANIM_SLOW_MS)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def apply_theme(self, theme: str) -> None:
        accent = config.PRIMARY_600 if theme == "light" else config.PRIMARY_400
        self.setStyleSheet(f"background-color: {accent};")  # accent from config PRIMARY_* (documented)

    def slide_to(self, x: int, width: int, y: int, animate: bool = True) -> None:
        target = QRect(x, y, width, _HEIGHT)
        if not animate or not config.ANIMATIONS_ENABLED:
            self.setGeometry(target)
            return
        self._anim.stop()
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(target)
        self._anim.start()
```

Wiring: on tab change, the view calls `slide_to` with the active tab's geometry (`tabRect` for a `QTabBar`, `widget.geometry()` for custom nav buttons); on resize and on mount, call it with `animate=False` (snap). The QSS selected-tab rule drops its own bottom border — the widget **is** the indicator (`rules/qss.md`).

> This widget is the single sanctioned expressive animation, and the accent it paints comes from the existing `config.PRIMARY_*` constants — no new color exception. With `config.ANIMATIONS_ENABLED = False` (reduced motion, §12) the underline snaps.

---

## 9. BUTTONS

| Variant    | Background    | Text          | Border           |
| ---------- | ------------- | ------------- | ---------------- |
| Primary    | `primary-600` | `onPrimary`   | none             |
| Secondary  | transparent   | `text`        | 1px `border`     |
| Danger     | `danger-600`  | #FFFFFF       | none             |
| Ghost      | transparent   | `text-subtle` | 1px transparent  |

**States per variant**:

| Variant    | hover                              | pressed       | disabled              |
| ---------- | ---------------------------------- | ------------- | --------------------- |
| Primary    | `primary-700`                      | `primary-800` | `opacity-disabled` 40% |
| Danger     | `danger-700`                       | `danger-800`  | `opacity-disabled` 40% |
| Secondary  | border → `border-strong`           | `bg-muted` bg | `opacity-disabled` 40% |
| Ghost      | border → `border`, text → `text`   | `bg-muted` bg | `opacity-disabled` 40% |

> v2.0: Secondary and Ghost hover by **stroke** (§8), no longer by `bg-muted` fill. Colored buttons keep their own darkening stops (`-700`/`-800`). `focus` shows the `focus-ring` on every variant.

> Primary button fill uses `primary-600` in **both** themes with `onPrimary` (unchanged v1.6 logic; the brighter `primary-400` remains reserved for dark foreground accents). Danger fill uses the light `danger-600` in both themes with white text; hover/pressed use the mode-agnostic `danger-700`/`danger-800`.

**Dynamic sizing** — unchanged from v1.6, the size results from content + padding:

| Size          | Vertical padding   | Horizontal padding | Font                   |
| ------------- | ------------------ | ------------------ | ---------------------- |
| `sm`          | `spacing-1` (4px)  | `spacing-3` (12px) | `medium` `xs` (12px)   |
| `md` (default)| `spacing-2` (8px)  | `spacing-4` (16px) | `medium` `sm` (14px)   |
| `lg`          | `spacing-3` (12px) | `spacing-6` (24px) | `medium` `base` (16px) |

**Aligned button group**: width unified on the widest button (`setMinimumWidth` on all).

---

## 10. ICONS — Lucide (vendored SVGs)

Library model: **vendored Lucide SVGs** in `resources/icons/` — only the icons the app actually uses, copied at generation time from the npm `lucide-static` package or the official Lucide repository (ISC license). Zero runtime icon dependency; the qtawesome path is retired with Font Awesome.

Stroke icons at 1.5–2px speak the same stroke language as the borders (§5); the framework stroke width is **1.75**.

**Rendering**: Lucide SVGs use `stroke="currentColor"`, which `QIcon` cannot resolve. The helper `utils/icons.py` (pure function, delivered with every app) loads the SVG text, substitutes the color and stroke width, and renders a `QIcon` via `QtSvg` (shipped with PySide6):

```python
# utils/icons.py — principle
def get_icon(name: str, color_key: str, theme: str, size: int) -> QIcon:
    """Load resources/icons/<name>.svg, recolor it (ICON_COLORS[theme][color_key]),
    set stroke-width 1.75, render at <size> px via QSvgRenderer."""
```

```python
# Usage in a view
from utils.icons import get_icon
icon = get_icon("house", "default", theme, config.ICON_MD)
```

**Colors**: all icon colors live in `config.ICON_COLORS` (per theme), never hardcoded in views or controllers — the documented exception to "all visual values in QSS". In v2.0 the values are the **derived** tokens (accent-tinted neutrals + per-project semantics):

```python
# config.py — example (Steel Blue default palette, derived values)
ICON_COLORS = {
    "light": {
        "default":  "#65717B",   # text-subtle
        "active":   PRIMARY_600,
        "success":  "#328F6D",   # success-600
        "warning":  "#A58327",   # warning-600
        "danger":   "#BA3B52",   # danger-600
        "info":     PRIMARY_600, # info = accent
        "muted":    "#98A4AE",   # text-muted
    },
    "dark": {
        "default":  "#94A2AD",   # text-subtle dark
        "active":   PRIMARY_400,
        "success":  "#6EC4A4",   # success-600 dark
        "warning":  "#D2B460",   # warning-600 dark
        "danger":   "#CB7282",   # danger-600 dark
        "info":     PRIMARY_400, # info = accent dark
        "muted":    "#5F6C77",   # text-muted dark
    }
}
ICON_STROKE: float = 1.75        # Lucide stroke width (design-system §10)
```

**Sizes**: use the tokens `icon-sm` (16px), `icon-md` (20px), `icon-lg` (24px) (`config.ICON_SM/MD/LG`).

**Vendoring rule**: every icon name used in a view must exist as `resources/icons/<name>.svg`. Standard set (toasts, theme, chrome): `circle-check`, `triangle-alert`, `circle-x`, `info`, `sun`, `moon`, `chevron-right`, `chevron-down`, `x`. Others are vendored on demand; verify the exact Lucide name against the source before copying — never invent one.

**Theme change**: icons are recreated on theme toggle (via `get_icon` with the new theme) — no dynamic color update on an existing instance.

---

## 11. QSS APPLICATION RULES

Unchanged from v1.6, plus rule 5.

1. **Zero hardcoded visual value in Python code.** Every color, size, font is in `styles_light.qss` / `styles_dark.qss` (documented exceptions in `config.py`: `PRIMARY_*`/`ON_PRIMARY`, `ICON_COLORS`, `SPLASH_COLORS`).
2. **Every styled widget has an `objectName`** matching a named QSS rule.
3. **Dark mode is handled by complete sheet replacement** (`styles_light.qss` → `styles_dark.qss`), not by partial override.
4. **Every QSS value is traced to a token in this file.** A `/* token : [name] */` comment indicates the source token.
5. **The signature underline is the only widget-painted visual** (§8): `views/sliding_underline.py` reads `config.PRIMARY_*` and `config.ANIM_SLOW_MS`; nothing else paints a themed color from code.

```qss
/* Example — token : bg / text */
QMainWindow {
    background-color: #FDFEFF;
    color: #0F181E;
}
```

---

## 12. ACCESSIBILITY

Target: **WCAG 2.1 level AA**.

| Criterion              | Rule                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Text contrast          | ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥ 18px bold or ≥ 24px) and UI components        |
| `text-muted` usage     | Disabled / decorative only — exempt from AA. Never for primary content                         |
| Statusbar text         | `text-subtle` (not `text-muted`). Essential/error status uses `text`                           |
| Semantic contrast      | Every derived `*-600` ≥ 3:1 against `bg` and against its `*-50` toast bg; error helper text ≥ 4.5:1 against `bg` |
| Semantic recognizability | Harmonization hue shift capped at ±6° (§2) — a danger stays red-family in every project      |
| Hover cue              | Border strengthening (§8) must yield a ≥ 3:1 change against the surface, or pair with the `bg-subtle` secondary cue |
| Minimum target size    | 24px. Button `sm` (~24px) is the floor; prefer `md` for touch-capable contexts                |
| Focus visibility       | `focus-ring` always visible on keyboard focus (§7), never removed                              |
| Reduced motion         | Respect the OS "show animations" setting via `config.ANIMATIONS_ENABLED`; when off, the drawer slide and the signature underline snap (no `QPropertyAnimation`) |

> Contrast figures are computed estimates, not tool-measured. Phase 1 runs the AA check on: text/bg, text-subtle/bg, accent/bg, onPrimary/accent, and each derived semantic pair; it reports failures without blocking (see `rules/config.md`).

---

## 13. LAYERING (stacking order)

Unchanged scale. Logical z-order from back to front; a persistent `danger` toast must never be hidden, so toasts sit above modals. v2.0 note: a floating layer is marked by its stroke — `border-strong` (or the toast's semantic accent) — plus `bg-elevated` on the surfaces that use it (drawer); **never** by a shadow.

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
