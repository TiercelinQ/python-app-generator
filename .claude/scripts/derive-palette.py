# Role: derive a project palette from one accent and run the WCAG AA check (design-system.md sections 2 and 12).
# Inputs: <accentHex> [--bg #hex] [--bg-subtle #hex] [--text #hex] [--border #hex]
#   The four overrides apply to the light theme; the dark theme keeps its tinted targets.
# Outputs: stdout = JSON { source, hue, accent, light, dark, adjusted, contrast, failures }; stderr = usage errors.
#   light and dark also carry the Qt literals: disabled-* and overlay.
#   adjusted = derived tokens moved by the AA floor (theme, token, from, to).
# Exit codes: 0 ok (contrast failures are reported, not blocking), 4 invalid argument.
# Command replaced: /python-p1-scoping, palette derivation and contrast check.
# Example: python .claude/scripts/derive-palette.py "#0D9488" --bg "#FFFDFB"
# Not for the default Steel Blue palette without override: the tables of design-system.md section 2 are canonical.

import json
import math
import re
import sys

OVERRIDES = ("--bg", "--bg-subtle", "--text", "--border")

# Tinted neutrals: (S, L) per theme, design-system.md section 2.
NEUTRALS = {
    "bg": {"light": (0, 100), "dark": (19, 8)},
    "bg-subtle": {"light": (27, 96), "dark": (17, 12)},
    "bg-elevated": {"dark": (17, 16)},
    "bg-muted": {"light": (25, 92), "dark": (17, 20)},
    "text": {"light": (33, 9), "dark": (24, 96)},
    "text-subtle": {"light": (11, 40), "dark": (13, 68)},
    "text-muted": {"light": (12, 64), "dark": (11, 42)},
    "border": {"light": (19, 86), "dark": (14, 26)},
    "border-subtle": {"light": (22, 91), "dark": (16, 20)},
    "border-strong": {"light": (14, 50), "dark": (16, 54)},
}

# Semantic anchors: hue, then (S, L) per theme.
SEMANTICS = {
    "success": {"hue": 152, "light": (48, 38), "dark": (42, 60)},
    "warning": {"hue": 38, "light": (62, 40), "dark": (56, 60)},
    "danger": {"hue": 355, "light": (52, 48), "dark": (46, 62)},
}

SURFACES = ("bg", "bg-subtle", "bg-elevated", "bg-muted")
STATUSES = ("success", "warning", "danger")
WHITE = "#FFFFFF"
DISABLED_OPACITY = 0.4


def fail(message):
    print(message, file=sys.stderr)
    print(
        "Usage: derive-palette.py <accentHex> [--bg #hex] [--bg-subtle #hex] [--text #hex] [--border #hex]",
        file=sys.stderr,
    )
    sys.exit(4)


def parse_hex(value, label):
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", value or "")
    if not match:
        fail(f"Invalid hex for {label}: {value or '(missing)'}")
    return "#" + match[1].upper()


def round_half_up(value):
    return math.floor(value + 0.5)


def to_rgb(color):
    return [int(color[i : i + 2], 16) for i in (1, 3, 5)]


def to_hex(rgb):
    return "#" + "".join(f"{round_half_up(c):02X}" for c in rgb)


def to_hsl(color):
    r, g, b = (c / 255 for c in to_rgb(color))
    high, low = max(r, g, b), min(r, g, b)
    light = (high + low) / 2
    delta = high - low
    if delta == 0:
        return (0, 0, light * 100)
    saturation = delta / (1 - abs(2 * light - 1))
    if high == r:
        hue = ((g - b) / delta + 6) % 6
    elif high == g:
        hue = (b - r) / delta + 2
    else:
        hue = (r - g) / delta + 4
    return (hue * 60, saturation * 100, light * 100)


def from_hsl(h, s, l):
    sat = s / 100
    light = min(100, max(0, l)) / 100
    a = sat * min(light, 1 - light)

    def channel(n):
        # Same expression as the electron script: it keeps both ports identical on .5 boundaries.
        k = (n + (((h % 360) + 360) % 360) / 30) % 12
        return (light - a * max(-1, min(k - 3, 9 - k, 1))) * 255

    return to_hex([channel(0), channel(8), channel(4)])


def mix(start, end, share):
    """sRGB mix: `share` is the part of `end` in the result."""
    return to_hex([a * (1 - share) + b * share for a, b in zip(to_rgb(start), to_rgb(end))])


def luminance(color):
    r, g, b = (c / 255 for c in to_rgb(color))
    r, g, b = (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in (r, g, b))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


def neutrals(hue, theme, overrides):
    out = {token: from_hsl(hue, *targets[theme]) for token, targets in NEUTRALS.items() if theme in targets}
    if theme == "light":
        if "--bg" in overrides:
            out["bg"] = overrides["--bg"]
        if "--bg-subtle" in overrides:
            out["bg-subtle"] = overrides["--bg-subtle"]
            h, s, l = to_hsl(overrides["--bg-subtle"])
            out["bg-muted"] = from_hsl(h, s, l - 3.5)
        if "--text" in overrides:
            out["text"] = overrides["--text"]
            out["text-subtle"] = mix(out["text"], out["bg"], 0.45)
            out["text-muted"] = mix(out["text"], out["bg"], 0.62)
        if "--border" in overrides:
            out["border"] = overrides["--border"]
            out["border-subtle"] = mix(out["border"], out["bg"], 0.5)
            out["border-strong"] = mix(out["border"], out["text"], 0.12)
        out["bg-elevated"] = out["bg"]
    out["bg-panel"] = out["bg-subtle"] if theme == "light" else out["bg-elevated"]
    return out


def floor(start, hsl, direction, pairs):
    """AA floor (design-system.md section 2): a derived token that fails moves by steps of 1 point of lightness
    until every pair passes; a token that passes keeps its value. Steps run on the integer lightness, which
    reproduces the named-palette table of design-system.md."""
    h, s, l = hsl

    def passes(color):
        return all(ratio(color, other) >= target for other, target in pairs)

    color = start
    lightness = round_half_up(l)
    while not passes(color) and 0 <= lightness + direction <= 100:
        lightness += direction
        color = from_hsl(h, s, lightness)
    return color, lightness


def semantic_hue(accent_hue, anchor):
    angle = (accent_hue - anchor + 540) % 360 - 180
    return anchor + max(-10, min(10, angle)) * 0.6


def parse_args(argv):
    overrides, positional = {}, []
    i = 0
    while i < len(argv):
        if argv[i] in OVERRIDES:
            overrides[argv[i]] = parse_hex(argv[i + 1] if i + 1 < len(argv) else None, argv[i])
            i += 2
        else:
            positional.append(argv[i])
            i += 1
    if len(positional) != 1:
        fail("Exactly one accent hex is expected.")
    return parse_hex(positional[0], "accent"), overrides


def derive(source, overrides):
    hue, saturation, _ = to_hsl(source)
    light = neutrals(hue, "light", overrides)
    dark = neutrals(hue, "dark", overrides)
    adjusted = []

    def settle(holder, theme, token, hsl, direction, pairs):
        previous = holder[token]
        color, lightness = floor(previous, hsl, direction, pairs)
        if color != previous:
            adjusted.append({"theme": theme, "token": token, "from": previous, "to": color})
        holder[token] = color
        return lightness

    for name, spec in SEMANTICS.items():
        h = semantic_hue(hue, spec["hue"])
        light[f"{name}-600"] = from_hsl(h, *spec["light"])
        dark[f"{name}-600"] = from_hsl(h, *spec["dark"])
        light[f"{name}-50"] = mix(light["bg"], light[f"{name}-600"], 0.08)
        dark[f"{name}-50"] = mix(dark["bg"], dark[f"{name}-600"], 0.18)

    accent = {
        "primary-50": from_hsl(hue, saturation, 95),
        "primary-400": from_hsl(hue, saturation, 70),
        "primary-600": source,
        "primary-900": from_hsl(hue, saturation, 25),
        "text-on-primary": WHITE,
        "text-on-danger": WHITE,
    }

    darkened = settle(
        accent,
        "accent",
        "primary-600",
        to_hsl(source),
        -1,
        [(WHITE, 4.5), (light["bg"], 4.5), (light["bg-subtle"], 4.5), (accent["primary-50"], 4.5)],
    )
    accent["primary-700"] = from_hsl(hue, saturation, darkened - 3)
    accent["primary-800"] = from_hsl(hue, saturation, darkened - 6)

    # Foreground neutrals move away from the canvas. Tokens chosen by the user are never moved.
    for name, theme in (("light", light), ("dark", dark)):
        direction = -1 if luminance(theme["text"]) < luminance(theme["bg"]) else 1
        surfaces = [theme[token] for token in SURFACES]
        soft = [theme[f"{status}-50"] for status in STATUSES]
        if name == "light":
            soft.append(accent["primary-50"])
        settle(theme, name, "text-subtle", to_hsl(theme["text-subtle"]), direction, [(c, 4.5) for c in surfaces + soft])
        settle(theme, name, "border-strong", to_hsl(theme["border-strong"]), direction, [(c, 3) for c in surfaces])

    settle(accent, "accent", "primary-400", (hue, saturation, 70), 1, [(dark["bg"], 4.5), (dark["bg-subtle"], 4.5)])
    settle(
        accent,
        "accent",
        "primary-900",
        (hue, saturation, 25),
        -1,
        [(accent["primary-400"], 4.5), (dark["text-subtle"], 4.5), (dark["text"], 4.5)],
    )

    light["info-600"] = accent["primary-600"]
    light["info-50"] = accent["primary-50"]
    dark["info-600"] = accent["primary-400"]
    dark["info-50"] = accent["primary-900"]

    danger_hue = semantic_hue(hue, SEMANTICS["danger"]["hue"])
    danger_s, danger_l = SEMANTICS["danger"]["light"]
    for theme in (light, dark):
        theme["danger-fill"] = light["danger-600"]
        theme["danger-700"] = from_hsl(danger_hue, danger_s, danger_l - 7)
        theme["danger-800"] = from_hsl(danger_hue, danger_s, danger_l - 13)

    # Qt literals: QSS has no opacity (design-system.md section 2, "Disabled colors and overlay").
    for theme in (light, dark):
        for token, color in (
            ("disabled-text", theme["text"]),
            ("disabled-text-subtle", theme["text-subtle"]),
            ("disabled-border-strong", theme["border-strong"]),
            ("disabled-primary", accent["primary-600"]),
            ("disabled-danger", theme["danger-fill"]),
            ("disabled-on-primary", WHITE),
        ):
            theme[token] = mix(theme["bg"], color, DISABLED_OPACITY)
        r, g, b = to_rgb(theme["text"])
        theme["overlay"] = f"rgba({r}, {g}, {b}, {round_half_up(255 * DISABLED_OPACITY)})"

    # Pairs of design-system.md section 12.
    contrast = []

    def check(theme_name, pair, foreground, background, target):
        value = ratio(foreground, background)
        contrast.append(
            {
                "theme": theme_name,
                "pair": pair,
                "ratio": float(f"{value:.2f}"),
                "target": target,
                "pass": value >= target,
            }
        )

    for name, theme in (("light", light), ("dark", dark)):
        primary = theme["info-600"]
        primary_bg = theme["info-50"]
        check(name, "text/bg", theme["text"], theme["bg"], 4.5)
        check(name, "text/primary-bg", theme["text"], primary_bg, 4.5)
        for surface in SURFACES:
            check(name, f"text-subtle/{surface}", theme["text-subtle"], theme[surface], 4.5)
            check(name, f"border-strong/{surface}", theme["border-strong"], theme[surface], 3)
        check(name, "text-subtle/primary-bg", theme["text-subtle"], primary_bg, 4.5)
        check(name, "primary/bg", primary, theme["bg"], 4.5)
        check(name, "primary/bg-subtle", primary, theme["bg-subtle"], 4.5)
        check(name, "primary/primary-bg", primary, primary_bg, 4.5)
        for stop in ("primary-600", "primary-700", "primary-800"):
            check(name, f"text-on-primary/{stop}", WHITE, accent[stop], 4.5)
        check(name, "text-on-danger/danger-fill", WHITE, theme["danger-fill"], 4.5)
        for status in STATUSES:
            check(name, f"text-subtle/{status}-50", theme["text-subtle"], theme[f"{status}-50"], 4.5)
        for status in (*STATUSES, "info"):
            # danger-600 is also the error helper text, hence the text threshold against bg.
            check(name, f"{status}-600/bg", theme[f"{status}-600"], theme["bg"], 4.5 if status == "danger" else 3)
            check(name, f"{status}-600/{status}-50", theme[f"{status}-600"], theme[f"{status}-50"], 3)
        # Qt only: tooltip text, and the focus ring drawn in `text` inside the filled buttons.
        check(name, "text/bg-elevated", theme["text"], theme["bg-elevated"], 4.5)
        check(name, "ring-text/primary-600", theme["text"], accent["primary-600"], 3)
        check(name, "ring-text/danger-fill", theme["text"], theme["danger-fill"], 3)

    return {
        "source": source,
        "hue": float(f"{hue:.2f}"),
        "accent": accent,
        "light": light,
        "dark": dark,
        "adjusted": adjusted,
        "contrast": contrast,
        "failures": [c for c in contrast if not c["pass"]],
    }


if __name__ == "__main__":
    print(json.dumps(derive(*parse_args(sys.argv[1:])), indent=2))
