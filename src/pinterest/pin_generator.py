#!/usr/bin/env python3
"""
PurePlated Automated Pinterest Pin Generator
--------------------------------------------
Generates high-converting, vertical (1000x1500 px, 2:3 aspect ratio) Pinterest Pins
using Pillow. Features editorial typography (DejaVu Serif + Sans), macro benefit badges,
and brand watermarking.
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECIPES_JSON = os.path.join(BASE_DIR, "src", "data", "recipes.json")
CONFIG_JSON = os.path.join(BASE_DIR, "config", "site_config.json")
PINS_DIR = os.path.join(BASE_DIR, "public", "assets", "pins")

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def generate_pin_for_recipe(recipe, config, output_path):
    width, height = 1000, 1500
    accent = recipe.get("color_accent", "#2D6A4F")

    # Base Canvas: Warm Linen / Off-White (#FDFBF7)
    img = Image.new("RGB", (width, height), "#FDFBF7")
    draw = ImageDraw.Draw(img)

    # 1. Outer Border / Frame
    margin = 32
    draw.rectangle(
        [(margin, margin), (width - margin, height - margin)],
        outline="#E5DFD3",
        width=2
    )

    # 2. Top Header Brand Bar
    header_font = get_font(SANS_BOLD, 22)
    header_text = "PUREPLATED  •  CLEAN & HEALTHY EASY MEALS"
    h_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    h_w = h_bbox[2] - h_bbox[0]
    draw.text(((width - h_w) / 2, 60), header_text, fill="#7A7569", font=header_font)

    # Divider line under header
    draw.line([(width // 2 - 120, 98), (width // 2 + 120, 98)], fill=accent, width=3)

    # 3. Category & Speed Eyebrow Pill
    cat_font = get_font(SANS_BOLD, 20)
    cat_text = f"{recipe.get('category', 'Healthy Meals').upper()}  •  {recipe.get('total_time', 20)} MINS"
    c_bbox = draw.textbbox((0, 0), cat_text, font=cat_font)
    c_w = c_bbox[2] - c_bbox[0]
    pill_padding = 24
    pill_w = c_w + (pill_padding * 2)
    pill_h = 42
    pill_x = (width - pill_w) / 2
    pill_y = 125

    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
        radius=21,
        fill=accent
    )
    draw.text((pill_x + pill_padding, pill_y + 10), cat_text, fill="#FFFFFF", font=cat_font)

    # 4. Bold Recipe Title (Editorial Serif)
    title = recipe.get("title", "")
    title_font = get_font(SERIF_BOLD, 52)
    max_title_width = width - 160
    title_lines = wrap_text(title, title_font, max_title_width, draw)

    y_text = 200
    for line in title_lines[:3]:
        t_bbox = draw.textbbox((0, 0), line, font=title_font)
        t_w = t_bbox[2] - t_bbox[0]
        draw.text(((width - t_w) / 2, y_text), line, fill="#1A202C", font=title_font)
        y_text += 68

    # 5. Recipe Subtitle / Headline
    headline = recipe.get("headline", "")
    if headline:
        head_font = get_font(SERIF_REG, 24)
        head_lines = wrap_text(headline, head_font, width - 200, draw)
        y_text += 10
        for line in head_lines[:2]:
            h_b = draw.textbbox((0, 0), line, font=head_font)
            h_w = h_b[2] - h_b[0]
            draw.text(((width - h_w) / 2, y_text), line, fill="#4A5568", font=head_font)
            y_text += 34

    # 6. Central Visual Hero Card Area (Framed Showcase)
    center_y = max(y_text + 30, 480)
    card_margin = 60
    card_h = 580
    card_rect = [(card_margin, center_y), (width - card_margin, center_y + card_h)]

    # Draw gradient-tinted background card for food visual
    draw.rounded_rectangle(card_rect, radius=18, fill="#F3EFE6", outline="#DDD5C7", width=2)

    # Decorative inner shadow effect / culinary vignette
    inner_margin = card_margin + 16
    inner_h = card_h - 32
    draw.rounded_rectangle(
        [(inner_margin, center_y + 16), (width - inner_margin, center_y + 16 + inner_h)],
        radius=14,
        fill="#EBE4D5"
    )

    # Central Culinary Icon / Badge
    center_box_w = 420
    center_box_h = 180
    cb_x = (width - center_box_w) / 2
    cb_y = center_y + (card_h - center_box_h) / 2 - 40

    draw.rounded_rectangle(
        [(cb_x, cb_y), (cb_x + center_box_w, cb_y + center_box_h)],
        radius=16,
        fill="#FFFFFF",
        outline=accent,
        width=3
    )

    chef_badge_font = get_font(SANS_BOLD, 18)
    draw.text((cb_x + 30, cb_y + 24), "★ CHEF TESTED & NUTRITIONIST APPROVED", fill=accent, font=chef_badge_font)

    time_callout = f"{recipe.get('total_time', 20)} MINUTE DINNER"
    time_font = get_font(SERIF_BOLD, 36)
    draw.text((cb_x + 30, cb_y + 58), time_callout, fill="#1A202C", font=time_font)

    easy_font = get_font(SANS_REG, 20)
    draw.text((cb_x + 30, cb_y + 115), "Low Prep  •  Easy Cleanup  •  Amazon Staples", fill="#555555", font=easy_font)

    # 7. High-Converting Macro & Benefit Badges (Horizontal Row of 4 Pills)
    badges_y = center_y + card_h - 120
    badges = [
        {"label": f"{recipe.get('protein', 0)}g", "sub": "PROTEIN", "color": accent},
        {"label": f"{recipe.get('calories', 0)}", "sub": "CALORIES", "color": "#1A202C"},
        {"label": f"{recipe.get('carbs', 0)}g", "sub": "CARBS", "color": "#7A7569"},
        {"label": f"{recipe.get('total_time', 0)}m", "sub": "TOTAL TIME", "color": "#D97706"}
    ]

    total_badges = len(badges)
    badge_w = 190
    badge_h = 80
    badge_spacing = 20
    total_row_w = (total_badges * badge_w) + ((total_badges - 1) * badge_spacing)
    start_bx = (width - total_row_w) / 2

    val_font = get_font(SANS_BOLD, 28)
    sub_font = get_font(SANS_BOLD, 14)

    for i, b in enumerate(badges):
        bx = start_bx + i * (badge_w + badge_spacing)
        draw.rounded_rectangle(
            [(bx, badges_y), (bx + badge_w, badges_y + badge_h)],
            radius=12,
            fill="#FFFFFF",
            outline="#D5CEC0",
            width=2
        )
        # Value text
        v_bbox = draw.textbbox((0, 0), b["label"], font=val_font)
        v_w = v_bbox[2] - v_bbox[0]
        draw.text((bx + (badge_w - v_w) / 2, badges_y + 14), b["label"], fill=b["color"], font=val_font)

        # Subtitle text
        s_bbox = draw.textbbox((0, 0), b["sub"], font=sub_font)
        s_w = s_bbox[2] - s_bbox[0]
        draw.text((bx + (badge_w - s_w) / 2, badges_y + 48), b["sub"], fill="#7A7569", font=sub_font)

    # 8. High-Impact Call To Action Box (Bottom)
    cta_y = center_y + card_h + 40
    cta_w = width - 120
    cta_h = 140
    cta_x = 60

    draw.rounded_rectangle(
        [(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
        radius=16,
        fill=accent
    )

    cta_heading_font = get_font(SANS_BOLD, 30)
    cta_sub_font = get_font(SANS_REG, 20)

    cta_heading = "TAP FOR RECIPE & SHOPPING LIST →"
    ch_bbox = draw.textbbox((0, 0), cta_heading, font=cta_heading_font)
    ch_w = ch_bbox[2] - ch_bbox[0]
    draw.text(((width - ch_w) / 2, cta_y + 32), cta_heading, fill="#FFFFFF", font=cta_heading_font)

    cta_sub = "Full Step-by-Step Instructions  •  Macros  •  Amazon Kitchen Tools"
    cs_bbox = draw.textbbox((0, 0), cta_sub, font=cta_sub_font)
    cs_w = cs_bbox[2] - cs_bbox[0]
    draw.text(((width - cs_w) / 2, cta_y + 82), cta_sub, fill="#E6F4EA", font=cta_sub_font)

    # 9. Clean Domain Footer Watermark
    footer_font = get_font(SANS_BOLD, 22)
    footer_text = "PUREPLATED.COM"
    f_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    f_w = f_bbox[2] - f_bbox[0]
    draw.text(((width - f_w) / 2, height - 80), footer_text, fill="#2D3748", font=footer_font)

    # Save PNG
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    return output_path

def generate_all_pins():
    with open(RECIPES_JSON, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    with open(CONFIG_JSON, "r", encoding="utf-8") as f:
        config = json.load(f)

    os.makedirs(PINS_DIR, exist_ok=True)
    print(f"\n=======================================================")
    print(f"      PUREPLATED PINTEREST PIN GENERATION STUDIO")
    print(f"=======================================================")

    generated = []
    for r in recipes:
        slug = r["id"]
        filename = f"pin-{slug}.png"
        out_path = os.path.join(PINS_DIR, filename)
        generate_pin_for_recipe(r, config, out_path)
        file_size = os.path.getsize(out_path) / 1024
        print(f"[✓] Generated 1000x1500 Pin: {filename:<45} ({file_size:.1f} KB)")
        generated.append(out_path)

    print(f"=======================================================")
    print(f"[✓] Successfully rendered {len(generated)} high-res Pinterest pins at {PINS_DIR}\n")
    return generated

if __name__ == "__main__":
    generate_all_pins()
