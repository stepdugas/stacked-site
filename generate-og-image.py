#!/usr/bin/env python3
"""Generate OG image (1200x630) for Stacked Flashcards website."""

from PIL import Image, ImageDraw, ImageFont

width, height = 1200, 630

# Dark background
img = Image.new('RGBA', (width, height), '#09090b')

# Subtle purple radial glow behind center
glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
cx, cy = width // 2, height // 2 - 30
for r in range(300, 0, -1):
    alpha = int(40 * (1 - r / 300) ** 2)
    glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 85, 247, alpha))
img = Image.alpha_composite(img, glow)
draw = ImageDraw.Draw(img)

# Load and center app icon at ~200x200
icon = Image.open('icon-512.png')
icon = icon.resize((200, 200), Image.LANCZOS)
icon_x = (width - 200) // 2
icon_y = 120
if icon.mode == 'RGBA':
    img.paste(icon, (icon_x, icon_y), icon)
else:
    img.paste(icon, (icon_x, icon_y))

# Load fonts (macOS Helvetica, fallback to default)
try:
    title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 72)
    sub_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 32)
except Exception:
    title_font = ImageFont.load_default()
    sub_font = ImageFont.load_default()

# "Stacked" in white, centered
title = 'Stacked'
bbox = draw.textbbox((0, 0), title, font=title_font)
tw = bbox[2] - bbox[0]
draw.text(((width - tw) // 2, 350), title, fill='white', font=title_font)

# "AI-Powered Flashcards" in gray, centered below
subtitle = 'AI-Powered Flashcards'
bbox2 = draw.textbbox((0, 0), subtitle, font=sub_font)
sw = bbox2[2] - bbox2[0]
draw.text(((width - sw) // 2, 440), subtitle, fill='#a1a1aa', font=sub_font)

# Save
img = img.convert('RGB')
img.save('og-image.png', 'PNG')
print('OG image created successfully: og-image.png (1200x630)')
