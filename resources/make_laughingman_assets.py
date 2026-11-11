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


def render_hour_bw_layers(size):
    source = Image.open(HANDS / f"f_hour_hand_color~{size}w.png").convert("RGBA")
    alpha = source.getchannel("A")
    mask = alpha.point(lambda value: 255 if value >= 128 else 0).convert("1")
    highlights = Image.new("1", source.size)

    pixels = source.load()
    highlight_pixels = [
        255 if (
            pixels[x, y][3] >= 128 and
            all(channel >= 192 for channel in pixels[x, y][:3])
        ) else 0
        for y in range(size)
        for x in range(size)
    ]
    highlights.putdata(highlight_pixels)
    return mask, highlights


def main():
    for size in SIZES:
        render_minute_hand(size, True).save(HANDS / f"f_minute_hand_color~{size}w.png")
        render_minute_hand(size, False).save(HANDS / f"f_minute_hand_bw~{size}w.png")

        mask, highlights = render_hour_bw_layers(size)
        mask.save(HANDS / f"f_hour_hand_mask_bw~{size}w.png")
        highlights.save(HANDS / f"f_hour_hand_highlight_bw~{size}w.png")

    for color in ("color", "bw"):
        Image.open(HANDS / f"f_hour_hand_{color}~144w.png").save(
            HANDS / f"f_hour_hand_{color}.png"
        )
    Image.open(HANDS / "f_hour_hand_mask_bw~144w.png").save(
        HANDS / "f_hour_hand_mask_bw.png"
    )
    Image.open(HANDS / "f_hour_hand_highlight_bw~144w.png").save(
        HANDS / "f_hour_hand_highlight_bw.png"
    )
    render_minute_hand(144, True).save(HANDS / "f_minute_hand_color.png")
    render_minute_hand(144, False).save(HANDS / "f_minute_hand_bw.png")


if __name__ == "__main__":
    main()
