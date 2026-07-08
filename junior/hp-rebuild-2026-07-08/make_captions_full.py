#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
W, H = 1600, 900
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CAPS = {
    "01-frontdoor": "HealthPilot  ·  the white-label engine behind Ted's Health",
    "12-studio":    "Customisation Studio  ·  tune it live, one embed snippet",
    "09-rebrand":   "One platform, any brand  ·  re-themed live",
    "13-quizflow":  "The patient assessment  ·  branded, to an AI report",
    "04-upsell":    "Results  →  a bookable next step, not a gate",
    "03-wearables": "Wearables  ·  objective data  (preview)",
    "07-escalations":"Clinical safety  ·  urgent flags + audit  (CQC)",
    "06-analytics": "The clinic's view  ·  a measurable channel",
    "10-owner":     "The platform  ·  usage, keys, versioned content",
    "11-close":     "HealthPilot  ×  Ted's Health",
}
FS = 30
font = ImageFont.truetype(FONT_PATH, FS)
accent = (18, 179, 166, 255)
box = (15, 42, 40, 232)
pad_x, pad_y, bar_w = 26, 16, 6
os.makedirs("captions-full", exist_ok=True)
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
    img.save(f"captions-full/{sid}.png")
    print("wrote", sid)
