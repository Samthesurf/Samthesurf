#!/usr/bin/env python3
"""Generate light and dark fastfetch-style SVG cards for Samuel's GitHub profile."""

from __future__ import annotations

import base64
from io import BytesIO
from calendar import monthrange
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import cast

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
AVATAR = ASSETS / "avatar.jpg"

WIDTH = 900
HEIGHT = 450
PORTRAIT_X = 18
PORTRAIT_Y = 58
PORTRAIT_SIZE = 340
INNER_PAD = 8
ASCII_COLS = 64
ASCII_ROWS = 32
ASCII_MARGIN_X = 9
ASCII_MARGIN_Y = 5
ASCII_CHARS = "@%#*+=-:. "

PROFILE = {
    "OS": "Arch Linux",
    "Kernel": "Linux 7.0.14",
    "Host": "Intel x86_64",
    "Editors": "Antigravity · Zed",
    "Agents": "Hermes Agent · Codex · OpenCode",
    "Focus": "Deep Learning · AI · Linux",
    "Stack": "Python · TypeScript · Dart · Lua",
    "GitHub": "@Samthesurf",
    "Repos": "Open source · ML · Linux",
    "Activity": "Contribution graph below",
}

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "panel": "#161b22",
        "panel2": "#0d1117",
        "border": "#30363d",
        "text": "#c9d1d9",
        "muted": "#8b949e",
        "blue": "#58a6ff",
        "purple": "#d2a8ff",
        "green": "#7ee787",
        "orange": "#ffa657",
        "red": "#ff7b72",
        "cyan": "#79c0ff",
    },
    "light": {
        "bg": "#ffffff",
        "panel": "#f6f8fa",
        "panel2": "#ffffff",
        "border": "#d0d7de",
        "text": "#24292f",
        "muted": "#57606a",
        "blue": "#0969da",
        "purple": "#8250df",
        "green": "#1a7f37",
        "orange": "#bc4c00",
        "red": "#cf222e",
        "cyan": "#0550ae",
    },
}


def add_months(value: datetime, months: int) -> datetime:
    year = value.year + (value.month - 1 + months) // 12
    month = (value.month - 1 + months) % 12 + 1
    day = min(value.day, monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def github_uptime(now: datetime | None = None) -> str:
    start = datetime(2021, 11, 20, 13, 52, 28, tzinfo=timezone.utc)
    now = now or datetime.now(timezone.utc)

    years = now.year - start.year
    anniversary = start.replace(year=start.year + years)
    if anniversary > now:
        years -= 1
        anniversary = start.replace(year=start.year + years)

    months = (now.year - anniversary.year) * 12 + now.month - anniversary.month
    cursor = add_months(anniversary, months)
    if cursor > now:
        months -= 1
        cursor = add_months(anniversary, months)

    remaining = now - cursor
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{years}y {months}mo {remaining.days}d {hours}h {minutes}m {seconds}s"


def avatar_canvas() -> Image.Image:
    source = Image.open(AVATAR).convert("RGB")
    corners = [source.getpixel((0, 0)), source.getpixel((source.width - 1, 0)),
               source.getpixel((0, source.height - 1)), source.getpixel((source.width - 1, source.height - 1))]
    background = tuple(sum(pixel[channel] for pixel in corners) // 4 for channel in range(3))
    # The original avatar is already tightly cropped around the face.
    # Add real canvas around it rather than zooming/cropping again.
    pad = round(max(source.size) * 0.20)
    canvas = Image.new("RGB", (source.width + pad * 2, source.height + pad * 2), background)
    canvas.paste(source, (pad, pad))
    return canvas


def sampled_avatar() -> Image.Image:
    canvas = ImageOps.contain(
        avatar_canvas(), (ASCII_COLS * 12, ASCII_ROWS * 24), Image.Resampling.LANCZOS
    )
    canvas = canvas.resize((ASCII_COLS, ASCII_ROWS), Image.Resampling.LANCZOS)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.18)
    canvas = ImageEnhance.Sharpness(canvas).enhance(1.25)
    return canvas


def portrait_image_uri() -> str:
    canvas = avatar_canvas()
    canvas.thumbnail((640, 640), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    canvas.save(buffer, format="JPEG", quality=86, optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def portrait_elements(mode: str) -> str:
    image = sampled_avatar()
    grayscale = image.convert("L")
    cell_width = (PORTRAIT_SIZE - INNER_PAD * 2) / ASCII_COLS
    cell_height = (PORTRAIT_SIZE - INNER_PAD * 2) / ASCII_ROWS
    font_size = cell_height * 0.94
    elements: list[str] = []

    for row in range(ASCII_ROWS):
        for col in range(ASCII_COLS):
            if (
                row < ASCII_MARGIN_Y
                or row >= ASCII_ROWS - ASCII_MARGIN_Y
                or col < ASCII_MARGIN_X
                or col >= ASCII_COLS - ASCII_MARGIN_X
            ):
                continue
            luminance = cast(int, grayscale.getpixel((col, row)))
            char_index = min(len(ASCII_CHARS) - 1, luminance * len(ASCII_CHARS) // 256)
            char = ASCII_CHARS[char_index]
            if char == " ":
                continue
            red, green, blue = cast(tuple[int, int, int], image.getpixel((col, row)))
            if mode == "dark":
                red = round(red * 0.76 + 255 * 0.24)
                green = round(green * 0.76 + 255 * 0.24)
                blue = round(blue * 0.76 + 255 * 0.24)
            else:
                red = round(red * 0.78)
                green = round(green * 0.78)
                blue = round(blue * 0.78)
            x = PORTRAIT_X + INNER_PAD + (col + 0.5) * cell_width
            y = PORTRAIT_Y + INNER_PAD + (row + 0.82) * cell_height
            opacity = 0.46 + ((255 - luminance) / 255) * 0.54

            elements.append(
                f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" '
                f'fill="#{red:02x}{green:02x}{blue:02x}" fill-opacity="{opacity:.3f}" '
                f'font-size="{font_size:.2f}">{escape(char)}</text>'
            )

    return "\n".join(elements)


def info_row(y: int, key: str, value: str, color: str, theme: dict[str, str]) -> str:
    return (
        f'<text x="394" y="{y}" fill="{theme[color]}" font-weight="700">{escape(key)}</text>'
        f'<text x="463" y="{y}" fill="{theme["muted"]}" fill-opacity="0.62">............</text>'
        f'<text x="548" y="{y}" fill="{theme["text"]}">{escape(value)}</text>'
    )


def build_svg(mode: str, generated_at: datetime) -> str:
    theme = THEMES[mode]
    uptime = github_uptime(generated_at)
    rows = [
        (135, "OS", PROFILE["OS"], "blue"),
        (157, "Kernel", PROFILE["Kernel"], "blue"),
        (179, "Host", PROFILE["Host"], "blue"),
        (201, "Uptime", uptime, "blue"),
        (253, "Editors", PROFILE["Editors"], "blue"),
        (275, "Agents", PROFILE["Agents"], "blue"),
        (297, "Focus", PROFILE["Focus"], "blue"),
        (319, "Stack", PROFILE["Stack"], "blue"),
        (371, "GitHub", PROFILE["GitHub"], "blue"),
        (393, "Repos", PROFILE["Repos"], "blue"),
        (415, "Activity", PROFILE["Activity"], "blue"),
    ]
    row_markup = "\n".join(info_row(*row, theme) for row in rows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">Samuel Ukpai's terminal-style GitHub profile</title>
  <desc id="desc">A full, uncropped colored ASCII portrait beside system, development, and GitHub information. Generated {generated_at:%Y-%m-%d %H:%M:%S} UTC.</desc>
  <defs>
    <clipPath id="portrait-clip"><rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{PORTRAIT_SIZE}" height="{PORTRAIT_SIZE}" rx="14"/></clipPath>
  </defs>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }}
  </style>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{theme['bg']}"/>
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="17" fill="none" stroke="{theme['border']}" stroke-width="2"/>
  <rect x="1" y="1" width="{WIDTH - 2}" height="42" rx="17" fill="{theme['panel']}"/>
  <path d="M1 42H899" stroke="{theme['border']}"/>
  <circle cx="24" cy="22" r="6" fill="#ff5f56"/><circle cx="44" cy="22" r="6" fill="#ffbd2e"/><circle cx="64" cy="22" r="6" fill="#27c93f"/>
  <text x="88" y="27" fill="{theme['muted']}" font-size="13">samuel@surf:~$ fastfetch</text>

  <rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{PORTRAIT_SIZE}" height="{PORTRAIT_SIZE}" rx="14" fill="{theme['panel2']}" stroke="{theme['border']}"/>
  <g clip-path="url(#portrait-clip)">
    <image x="{PORTRAIT_X + INNER_PAD}" y="{PORTRAIT_Y + INNER_PAD}" width="{PORTRAIT_SIZE - INNER_PAD * 2}" height="{PORTRAIT_SIZE - INNER_PAD * 2}" preserveAspectRatio="xMidYMid meet" opacity="0.68" href="{portrait_image_uri()}"/>
    <g>{portrait_elements(mode)}</g>
  </g>
  <path d="M374 64V424" stroke="{theme['border']}"/>

  <text x="394" y="82" fill="{theme['cyan']}" font-size="24" font-weight="700">samuel@surf</text>
  <text x="590" y="82" fill="{theme['muted']}" font-size="13">~/github/profile</text>
  <path d="M394 96H868" stroke="{theme['border']}"/>

  <text x="394" y="112" fill="{theme['muted']}" font-size="10" font-weight="700" letter-spacing="2">SYSTEM</text>
  <text x="394" y="230" fill="{theme['muted']}" font-size="10" font-weight="700" letter-spacing="2">WORKSPACE</text>
  <text x="394" y="348" fill="{theme['muted']}" font-size="10" font-weight="700" letter-spacing="2">GITHUB</text>

  <g font-size="14">{row_markup}</g>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0)
    for mode in THEMES:
        (ASSETS / f"profile-{mode}.svg").write_text(build_svg(mode, generated_at), encoding="utf-8")
    print(f"Generated profile cards at {generated_at:%Y-%m-%d %H:%M:%S} UTC")


if __name__ == "__main__":
    main()
