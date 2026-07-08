#!/usr/bin/env python3
"""Render lower-third caption PNG overlays (1600x900, transparent) per scene."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1600, 900
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CAPS = {
    "01-landing":    "HealthPilot  ·  the white-label health platform",
    "02-intake":     "Guided patient intake  ·  premium on every screen",
    "03-whitelabel": "Live white-label theming  ·  one platform, any brand",
    "04-owner":      "Clinic owner console  ·  fully self-serve",
    "05-close":      "HealthPilot  ×  Ted's Health",
}
FS = 30
font = ImageFont.truetype(FONT_PATH, FS)
accent = (18, 179, 166, 255)   # teal accent bar
box = (15, 42, 40, 228)        # deep teal pill
pad_x, pad_y = 26, 16
bar_w = 6
os.makedirs("captions", exist_ok=True)

for sid, text in CAPS.items():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    box_w = bar_w + pad_x + tw + pad_x
    box_h = pad_y + th + pad_y
    x0, y0 = 64, H - 96 - box_h
    d.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=14, fill=box)
    d.rectangle([x0, y0 + 8, x0 + bar_w, y0 + box_h - 8], fill=accent)
    d.text((x0 + bar_w + pad_x - l, y0 + pad_y - t), text, font=font, fill=(255, 255, 255, 255))
    out = f"captions/{sid}.png"
    img.save(out)
    print("wrote", out)
