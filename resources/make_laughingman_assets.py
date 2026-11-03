#!/usr/bin/env python3

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
HANDS = ROOT / "clock_hands"
FONT = ROOT / "ArchivoNarrow-Bold.ttf"
TEXT = (ROOT.parent / "laughingman.txt").read_text(encoding="utf-8").splitlines()[0]
SIZES = (144, 180, 200, 260)
BLUE = (0, 85, 119, 255)


def render_minute_hand(size, color):
    scale = 4
    canvas_size = size * scale
    image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    center = canvas_size // 2
    foreground = BLUE if color else (0, 0, 0, 255)

    font_size = round(size * 0.078 * scale)
    enlarged_i_size = round(font_size * 3.5)
    fonts = [
        ImageFont.truetype(FONT, enlarged_i_size if character == "I" and index == 0 else font_size)
        for index, character in enumerate(TEXT)
    ]
    widths = [font.getlength(character) for font, character in zip(fonts, TEXT)]
    circumference = 2 * math.pi * (size * 0.342 * scale)
    text_scale = min(1.0, circumference * 0.96 / sum(widths))
    text_radius = size * 0.342 * scale
    distance = -sum(widths) * text_scale / 2

    for character, font, width in zip(TEXT, fonts, widths):
        half_width = width * text_scale / 2
        distance += half_width
        angle = distance / text_radius
        x = center + text_radius * math.cos(angle)
        y = center + text_radius * math.sin(angle)

        glyph = Image.new("RGBA", (round(width) + font_size * 2, font_size * 4), (0, 0, 0, 0))
        glyph_draw = ImageDraw.Draw(glyph)
        glyph_draw.text((glyph.width // 2, glyph.height // 2), character, font=font,
                        fill=foreground, anchor="mm")
        glyph = glyph.resize((round(glyph.width * text_scale), glyph.height), Image.Resampling.LANCZOS)
        glyph = glyph.rotate(-(angle * 180 / math.pi + 90), resample=Image.Resampling.BICUBIC,
                             expand=True)
        image.alpha_composite(glyph, (round(x - glyph.width / 2), round(y - glyph.height / 2)))
        distance += half_width

    image = image.resize((size, size), Image.Resampling.LANCZOS)
    if color:
        return image
    monochrome = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    monochrome.alpha_composite(image)
    return monochrome.convert("L").point(lambda value: 255 if value > 127 else 0).convert("1")


def main():
    for size in SIZES:
        render_minute_hand(size, True).save(HANDS / f"f_minute_hand_color~{size}w.png")
        render_minute_hand(size, False).save(HANDS / f"f_minute_hand_bw~{size}w.png")
    for hand in ("hour", "minute"):
        render_minute_hand(144, True).save(HANDS / f"f_{hand}_hand_color.png")
        render_minute_hand(144, False).save(HANDS / f"f_{hand}_hand_bw.png")


if __name__ == "__main__":
    main()
