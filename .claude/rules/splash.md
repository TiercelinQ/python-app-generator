# Splash screen rules — Python/PyQt6 app

> Conditional — only when Phase 3 "Splash screen" = `Yes`. A splash is a short launch window (`QSplashScreen`) shown while the main window boots, then dismissed. Opt-in, decided in Phase 3, locked in the Phase 4 contract, implemented in Phase 5. When disabled: no splash file, no config constant, the main window shows normally.

The splash follows the design system (flat, palette, dark mode) like the rest of the UI. It shows the **application icon if one is defined**, otherwise the application name centered (text-only).

## Icon source

- The splash reuses the **application icon** captured in Phase 1 (Q6, `resources/icon.ico`).
- If no icon was defined in Phase 1 and the splash is enabled, Phase 3 offers an **optional icon path** (free-form). A provided image is saved as `resources/icon.ico` and becomes the app icon everywhere (window/taskbar via `app.setWindowIcon`, packaging via `build.spec`) — not a splash-only asset.
- No icon at all → the splash shows the application name only. Never a placeholder image.

## Colors — documented exception in `config.py`

`QSplashScreen` is painted programmatically (its pixmap is built in Python), so its background/text colors **cannot** be styled via QSS. Like `ICON_COLORS` (qtawesome), the splash colors live in `config.py` — the second documented exception to "all visual values in QSS". Derived from the palette neutrals (`bg`/`text`), per theme:

```python
# Splash (if enabled in Phase 3) — painted programmatically, not QSS-stylable (documented exception, like ICON_COLORS)
SPLASH_MIN_DURATION_MS: int = 1200            # minimum on-screen time before dismissal
SPLASH_COLORS: dict = {
    "light": {"bg": "#FFFFFF", "text": "#111827"},   # bg / text (light neutrals)
    "dark":  {"bg": "#1C1C1C", "text": "#F5F5F5"},   # bg / text (dark neutrals)
}
```

Keep these in sync with the `bg`/`text` neutrals of `styles_light.qss` / `styles_dark.qss` (a custom palette replaces them). The min duration avoids a flash on fast startup: the splash stays at least `SPLASH_MIN_DURATION_MS`, then closes once the main window is shown.

## View — `views/splash_screen.py`

A small factory (PyQt6 only, no business logic) that builds the `QSplashScreen`:

```python
"""Splash screen — launch window shown until the main window is ready."""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QSplashScreen

import config

_SPLASH_SIZE = (420, 260)
_ICON_PATH = Path("resources/icon.ico")


def create_splash(theme: str) -> QSplashScreen:
    """Build the splash for the given theme ("light"/"dark").

    Shows the app icon if resources/icon.ico exists, otherwise the app name.
    Colors come from config.SPLASH_COLORS (QSplashScreen is painted, not QSS-stylable).
    """
    colors = config.SPLASH_COLORS[theme]
    pixmap = QPixmap(*_SPLASH_SIZE)
    pixmap.fill(QColor(colors["bg"]))

    painter = QPainter(pixmap)
    try:
        if _ICON_PATH.exists():
            icon = QPixmap(str(_ICON_PATH)).scaled(
                96, 96, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (pixmap.width() - icon.width()) // 2
            painter.drawPixmap(x, 60, icon)
        else:
            painter.setPen(QColor(colors["text"]))
            painter.setFont(QFont("", 20, QFont.Weight.Medium))
            painter.drawText(
                pixmap.rect(), Qt.AlignmentFlag.AlignCenter, config.APP_NAME
            )
    finally:
        painter.end()

    return QSplashScreen(pixmap)
```

- Flat: `pixmap.fill` with the themed neutral, no shadow/gradient/rounded corner — consistent with `@rules/qss.md` flat design.
- No `objectName` (a `QSplashScreen` pixmap is not a styled QSS widget).

## Orchestration — `main.py`

Insert the splash into the strict init order, before the `MainWindow`, and dismiss it after the window is shown (respecting the min duration):

```python
from PyQt6.QtCore import QTimer

setup_logging()
run_migrations()                          # if DB
app = QApplication(sys.argv)
app.setStyle("Fusion")                    # mandatory — @rules/qss.md
install_translator(app)                   # if i18n

theme = _resolve_startup_theme()          # persisted preference, else OS
splash = create_splash(theme)             # if splash enabled — @rules/splash.md
splash.show()
app.processEvents()                       # paint the splash immediately

window = MainWindow()
install_excepthook(window)
window.show()
QTimer.singleShot(
    config.SPLASH_MIN_DURATION_MS, lambda: splash.finish(window)
)
sys.exit(app.exec())
```

- `splash.finish(window)` closes the splash and raises the main window. The `QTimer.singleShot` enforces the minimum on-screen time; `MainWindow()` construction happens meanwhile so startup is not delayed beyond it.
- `_resolve_startup_theme()` reads the persisted `theme` preference (if preferences enabled) or falls back to the OS theme — same source the QSS sheet selection uses.

## Anti-patterns — what NOT to do

- **Do not** put the splash bg/text colors in QSS or hardcode them in `splash_screen.py` — read `config.SPLASH_COLORS` (the one documented exception, like `ICON_COLORS`).
- **Do not** add business logic to `views/splash_screen.py` — it builds a pixmap and returns the splash.
- **Do not** block on the splash (no `app.exec()` loop, no modal) — it self-dismisses via `splash.finish(window)`.
- **Do not** load a remote image — the icon is the local `resources/icon.ico`.
- **Do not** add a shadow, gradient, or rounded corner to the splash — flat design is global (`@rules/qss.md`).
- **Do not** ship the splash when Phase 3 "Splash screen" = No (no file, no `SPLASH_*` constant).

## Integrity verification

Detailed in `@rules/verification.md`. Key points (if splash enabled): `views/splash_screen.py` present (PyQt6 only, no business logic); `SPLASH_MIN_DURATION_MS` + `SPLASH_COLORS` in `config.py`; `create_splash` called in `main.py` before `MainWindow`, dismissed via `splash.finish(window)` after the min duration; colors read from `config.SPLASH_COLORS` (no hardcoded value in the view); icon resolved to `resources/icon.ico` or text-only fallback.
