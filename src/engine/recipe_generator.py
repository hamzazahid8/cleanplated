#!/usr/bin/env python3
"""
PurePlated Autonomous Daily Recipe Generator
--------------------------------------------
Generates complete, nutritious, macro-balanced everyday recipes.
Automatically computes macros, maps Amazon kitchen tools & pantry staples,
synthesizes Pinterest pin copy, creates the 1000x1500 pin graphic,
and triggers the static site build.
"""

import os
import sys
import json
import random
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from src.pinterest.pin_generator import generate_pin_for_recipe
from src.engine.build_site import build_all

RECIPES_JSON = os.path.join(BASE_DIR, "src", "data", "recipes.json")
CONFIG_JSON = os.path.join(BASE_DIR, "config", "site_config.json")
PINS_DIR = os.path.join(BASE_DIR, "public", "assets", "pins")

# Curated Culinary Synthesis Matrix for Easy Healthy Meals
PROTEINS = [
    {"name": "Wild-Caught Salmon Fillet", "cals_per_100g": 180, "p": 25, "f": 8, "c": 0, "tag": "salmon"},
    {"name": "Chicken Breast Tenderloins", "cals_per_100g": 120, "p": 26, "f": 2, "c": 0, "tag": "chicken"},
    {"name": "Lean Ground Turkey (93/7)", "cals_per_100g": 150, "p": 22, "f": 7, "c": 0, "tag": "turkey"},
    {"name": "Jumbo Wild Gulf Shrimp", "cals_per_100g": 99, "p": 24, "f": 1, "c": 0, "tag": "shrimp"},
    {"name": "Grass-Fed Sirloin Steak Bites", "cals_per_100g": 170, "p": 26, "f": 7, "c": 0, "tag": "beef"},
    {"name": "Organic Extra Firm Tofu", "cals_per_100g": 95, "p": 12, "f": 5, "c": 2, "tag": "vegetarian"}
]

VEGETABLES = [
    {"name": "Garlic Butter Asparagus Spears", "cals": 45, "p": 4, "c": 5, "f": 1, "tool": "skillet"},
    {"name": "Crispy Air-Fried Broccoli Florets", "cals": 55, "p": 5, "c": 7, "f": 1, "tool": "air_fryer"},
    {"name": "Zesty Ribboned Zucchini Noodles", "cals": 30, "p": 2, "c": 5, "f": 0, "tool": "veggie_chopper"},
    {"name": "Blistered Mini Sweet Peppers", "cals": 40, "p": 2, "c": 8, "f": 0, "tool": "skillet"},
    {"name": "Roasted Garlic Cauliflower Rice", "cals": 40, "p": 3, "c": 6, "f": 1, "tool": "skillet"},
    {"name": "Mediterranean Cucumber Cherry Tomato Salad", "cals": 50, "p": 2, "c": 8, "f": 1, "tool": "chef_knife"}
]

FLAVOR_STYLES = [
    {
        "style": "Lemon Herb & Garlic",
        "cuisine": "Mediterranean",
        "category": "Quick 20-Min Dinners",
        "color": "#2D6A4F",
        "pantry": ["olive_oil", "himalayan_salt"],
        "adjectives": ["Zesty", "Herb-Crusted", "Crispy", "Garlic Butter"],
        "aromatics": "minced fresh garlic, chopped Italian parsley, dried oregano, and fresh lemon juice"
    },
    {
        "style": "Smoky Chipotle & Avocado Lime",
        "cuisine": "Mexican-Inspired",
        "category": "High-Protein Meals",
        "color": "#E76F51",
        "pantry": ["avocado_oil_spray", "himalayan_salt"],
        "adjectives": ["Sizzling", "Chipotle Spiced", "Fiesta", "Smoky"],
        "aromatics": "smoked paprika, ground cumin, chili powder, fresh lime juice, and avocado crema"
    },
    {
        "style": "Honey Ginger Soy Glaze",
        "cuisine": "Asian-Fusion",
        "category": "Meal Prep & Bowls",
        "color": "#D97706",
        "pantry": ["avocado_oil_spray", "himalayan_salt"],
        "adjectives": ["Sweet & Savory", "Caramelized", "Glazed", "Sticky Garlic"],
        "aromatics": "fresh grated ginger, minced garlic, low-sodium tamari, raw clover honey, and toasted sesame"
    },
    {
        "style": "Parmesan & Cracked Black Pepper Crunch",
        "cuisine": "Italian-American",
        "category": "Air Fryer Clean Eats",
        "color": "#2A9D8F",
        "pantry": ["olive_oil", "himalayan_salt"],
        "adjectives": ["Golden", "Parmesan Crusted", "Extra Crispy", "Oven-Baked"],
        "aromatics": "finely grated aged parmesan, garlic powder, crushed black peppercorns, and olive oil"
    }
]

def synthesize_new_recipe(existing_slugs):
    flavor = random.choice(FLAVOR_STYLES)
    protein = random.choice(PROTEINS)
    veg = random.choice(VEGETABLES)

    adj = random.choice(flavor["adjectives"])
    cook_method = random.choice(["Air Fryer", "One-Pan", "15-Minute", "Sheet Pan", "Skillet"])
    title = f"{adj} {cook_method} {protein['name'].split()[0]} with {veg['name']}"
    
    slug = title.lower().replace("&", "and").replace("'", "")
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')

    if slug in existing_slugs:
        slug = f"{slug}-{random.randint(10, 99)}"

    prep_time = random.choice([5, 8, 10])
    cook_time = random.choice([8, 10, 12, 14])
    total_time = prep_time + cook_time
    servings = 2

    prot_grams = int(protein["p"] * 1.6 + veg["p"] + 4)
    cal_count = int(protein["cals_per_100g"] * 1.8 + veg["cals"] + 120)
    carb_grams = int(veg["c"] + random.randint(2, 6))
    fat_grams = int(protein["f"] * 1.6 + 10)
    fiber_grams = int(random.randint(3, 5))

    headline = f"Tender {protein['name'].lower()} seared in {flavor['aromatics']}, served alongside {veg['name'].lower()} in only {total_time} minutes."

    ingredients = [
        {"amount": 1, "unit": "lb", "item": protein["name"], "notes": "patted dry with paper towels"},
        {"amount": 1, "unit": "large bunch", "item": veg["name"], "notes": "trimmed and chopped into bite-sized pieces"},
        {"amount": 1.5, "unit": "tbsp", "item": "Extra Virgin Olive Oil", "amazon_key": "olive_oil"},
        {"amount": 3, "unit": "cloves", "item": "Fresh Garlic", "notes": "finely minced"},
        {"amount": 1, "unit": "tsp", "item": "Artisanal Seasoning Blend", "notes": flavor["style"]},
        {"amount": 0.5, "unit": "tsp", "item": "Ancient Sea Salt", "amazon_key": "himalayan_salt"},
        {"amount": 0.25, "unit": "tsp", "item": "Cracked Black Pepper"}
    ]

    instructions = [
        {
            "step": 1,
            "title": f"Prep the {protein['name'].split()[0]} and Veggies",
            "text": f"Pat the {protein['name'].lower()} completely dry with paper towels. Trim and prepare {veg['name'].lower()} on a clean cutting board."
        },
        {
            "step": 2,
            "title": "Season with Aromatics",
            "text": f"In a small prep bowl, combine olive oil, minced garlic, sea salt, pepper, and {flavor['aromatics']}. Rub evenly over the {protein['name'].lower()} and toss with the {veg['name'].lower()}."
        },
        {
            "step": 3,
            "title": "Cook Over High Heat",
            "text": f"Preheat your pan or air fryer to 400°F (200°C). Cook {protein['name'].lower()} for 8–10 minutes, flipping halfway until internal temperature reaches recommended safe temp."
        },
        {
            "step": 4,
            "title": "Combine and Garnish",
            "text": f"Plate the warm {protein['name'].lower()} alongside {veg['name'].lower()}. Drizzle with any remaining pan juices, garnish with fresh herbs, and serve hot."
        }
    ]

    tools = ["skillet", "chef_knife"]
    if veg.get("tool") in ["air_fryer", "veggie_chopper"]:
        tools.append(veg["tool"])
    if "Air Fryer" in title:
        tools.insert(0, "air_fryer")
    tools = list(dict.fromkeys(tools))[:3]

    pin_title = f"{title} ({prot_grams}g Protein & {total_time} Mins)"
    pin_desc = f"{adj} {protein['name'].lower()} and {veg['name'].lower()} made in only {total_time} minutes! Packed with {prot_grams}g protein and low carb. Tap for full recipe and tools list! #healthymeals #highprotein #quickdinner #easyrecipes"

    new_recipe = {
        "id": slug,
        "title": title,
        "headline": headline,
        "category": flavor["category"],
        "cuisine": flavor["cuisine"],
        "difficulty": "Easy",
        "prep_time": prep_time,
        "cook_time": cook_time,
        "total_time": total_time,
        "servings": servings,
        "calories": cal_count,
        "protein": prot_grams,
        "carbs": carb_grams,
        "fat": fat_grams,
        "fiber": fiber_grams,
        "badges": [f"⏱️ {total_time} Mins", f"💪 {prot_grams}g Protein", "🥗 Clean Eats", f"🔥 {cal_count} Cals"],
        "tags": [protein["tag"], "dinner", "high-protein", "healthy", "quick-meal"],
        "hero_image": f"/assets/images/recipes/{slug}.jpg",
        "pin_image": f"/assets/pins/pin-{slug}.png",
        "color_accent": flavor["color"],
        "description": f"This wholesome {title} delivers the perfect balance of lean protein, crisp fresh vegetables, and vibrant {flavor['cuisine'].lower()} flavor in only {total_time} minutes of total time.",
        "why_it_works": [
            f"Delivers {prot_grams}g of clean muscle-building protein per serving.",
            f"Ready from start to finish in just {total_time} minutes.",
            "Uses wholesome pantry staples available with fast Amazon delivery."
        ],
        "ingredients": ingredients,
        "instructions": instructions,
        "chef_tips": [
            "Always pat proteins dry with a paper towel before cooking to get a golden caramelized crust.",
            "Do not overcrowd your pan or air fryer basket to ensure high-heat roasting rather than steaming."
        ],
        "recommended_tools": tools,
        "recommended_pantry": flavor["pantry"],
        "pin_copy": {
            "title": pin_title,
            "description": pin_desc,
            "board": "Quick & Healthy Easy Meals"
        }
    }
    return new_recipe

def generate_and_publish_daily_recipe():
    with open(RECIPES_JSON, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    with open(CONFIG_JSON, "r", encoding="utf-8") as f:
        config = json.load(f)

    existing_slugs = set(r["id"] for r in recipes)
    new_r = synthesize_new_recipe(existing_slugs)
    recipes.append(new_r)

    with open(RECIPES_JSON, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2)

    print(f"\n[✓] Generated New Daily Recipe: '{new_r['title']}'")
    print(f"    Category: {new_r['category']} | Total Time: {new_r['total_time']}m | Protein: {new_r['protein']}g | Calories: {new_r['calories']}")

    # 1. Render Pinterest Pin
    pin_filename = f"pin-{new_r['id']}.png"
    pin_out = os.path.join(PINS_DIR, pin_filename)
    generate_pin_for_recipe(new_r, config, pin_out)
    print(f"[✓] Created High-Res Pinterest Pin at {pin_out}")

    # 2. Recompile static site, sitemap, and Pinterest feed
    build_all()
    print(f"[✓] Entire website and Pinterest RSS feed updated successfully with new daily recipe!\n")
    return new_r

if __name__ == "__main__":
    generate_and_publish_daily_recipe()
