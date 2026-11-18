#!/usr/bin/env python3
"""
PurePlated Static Site Compiler & Automation Engine
--------------------------------------------------
Compiles recipes into lightning-fast, SEO-optimized HTML pages,
complete with Google Recipe JSON-LD schema, interactive serving scalers,
Amazon Affiliate product showcases, XML sitemaps, and Pinterest RSS feeds.
"""

import os
import json
import re
from datetime import datetime
from xml.sax.saxutils import escape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECIPES_JSON = os.path.join(BASE_DIR, "src", "data", "recipes.json")
CONFIG_JSON = os.path.join(BASE_DIR, "config", "site_config.json")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
RECIPES_DIR = os.path.join(PUBLIC_DIR, "recipes")
CATEGORY_DIR = os.path.join(PUBLIC_DIR, "category")
FEED_DIR = os.path.join(PUBLIC_DIR, "feed")

def load_data():
    with open(RECIPES_JSON, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    with open(CONFIG_JSON, "r", encoding="utf-8") as f:
        config = json.load(f)
    return recipes, config

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text)

# Shared Stylesheet & UI Components
BASE_CSS = """
:root {
  --bg: #FBFBFA;
  --surface: #FFFFFF;
  --surface-alt: #F4F1EA;
  --ink: #1A202C;
  --ink-secondary: #4A5568;
  --ink-muted: #718096;
  --border: #E2DDD5;
  --accent: #2D6A4F;
  --accent-light: #EBF5F0;
  --accent-hover: #1B4332;
  --gold: #D97706;
  --gold-light: #FEF3C7;
  --amazon-orange: #FF9900;
  --amazon-hover: #E68A00;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -1px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.03);
  --font-serif: "DejaVu Serif", Georgia, "Times New Roman", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background-color: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a { color: inherit; text-decoration: none; }
img { max-width: 100%; height: auto; display: block; }

.container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Site Header */
.site-header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 72px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent);
}
.brand span { color: var(--gold); }
.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
  font-weight: 500;
  font-size: 0.95rem;
  color: var(--ink-secondary);
}
.nav-links a:hover { color: var(--accent); }
.nav-cta {
  background: var(--accent);
  color: #fff !important;
  padding: 8px 18px;
  border-radius: 6px;
  font-weight: 600;
  transition: background 0.2s;
}
.nav-cta:hover { background: var(--accent-hover); }

/* Hero Section */
.hero {
  padding: 56px 0 40px;
  text-align: center;
  background: linear-gradient(180deg, var(--surface) 0%, var(--bg) 100%);
  border-bottom: 1px solid var(--border);
}
.hero-tag {
  display: inline-block;
  background: var(--accent-light);
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 20px;
  margin-bottom: 16px;
}
.hero h1 {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.2;
  color: var(--ink);
  max-width: 820px;
  margin: 0 auto 16px;
}
.hero p {
  font-size: 1.15rem;
  color: var(--ink-secondary);
  max-width: 640px;
  margin: 0 auto 28px;
}

/* Category Filter Bar */
.filter-bar {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 16px 0;
  margin-bottom: 36px;
  scrollbar-width: none;
}
.filter-bar::-webkit-scrollbar { display: none; }
.filter-btn {
  padding: 8px 18px;
  border-radius: 24px;
  background: var(--surface);
  border: 1px solid var(--border);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--ink-secondary);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}
.filter-btn:hover, .filter-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

/* Recipe Grid */
.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 28px;
  margin-bottom: 60px;
}
.recipe-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}
.recipe-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.card-media {
  position: relative;
  height: 220px;
  background: var(--surface-alt);
  overflow: hidden;
}
.card-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.card-badge-top {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(26, 32, 44, 0.85);
  backdrop-filter: blur(4px);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 4px;
  letter-spacing: 0.04em;
}
.card-time {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.92);
  color: var(--ink);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 4px;
  box-shadow: var(--shadow-sm);
}
.card-body {
  padding: 22px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.card-category {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}
.card-title {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  line-height: 1.35;
  color: var(--ink);
  margin-bottom: 10px;
}
.card-desc {
  font-size: 0.9rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  margin-bottom: 16px;
  flex: 1;
}
.card-macros {
  display: flex;
  gap: 12px;
  padding-top: 14px;
  border-top: 1px solid var(--border);
  font-size: 0.8rem;
  color: var(--ink-muted);
}
.card-macros b { color: var(--accent); }

/* Amazon Featured Showcase on Homepage */
.amazon-showcase {
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  margin: 60px 0;
}
.showcase-header {
  text-align: center;
  max-width: 600px;
  margin: 0 auto 36px;
}
.showcase-header h2 {
  font-family: var(--font-serif);
  font-size: 1.8rem;
  color: var(--ink);
  margin-bottom: 8px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}
.tool-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
}
.tool-card:hover { transform: translateY(-2px); }
.tool-badge {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 8px;
}
.tool-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 8px;
  line-height: 1.3;
}
.tool-desc {
  font-size: 0.82rem;
  color: var(--ink-secondary);
  margin-bottom: 16px;
  flex: 1;
}
.amazon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--amazon-orange);
  color: #111;
  font-weight: 700;
  font-size: 0.82rem;
  padding: 10px 14px;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s;
}
.amazon-btn:hover { background: var(--amazon-hover); }

/* Recipe Detail Layout */
.recipe-page {
  padding: 40px 0 80px;
}
.breadcrumbs {
  font-size: 0.85rem;
  color: var(--ink-muted);
  margin-bottom: 20px;
}
.breadcrumbs a:hover { color: var(--accent); }
.recipe-header {
  margin-bottom: 28px;
}
.recipe-header h1 {
  font-family: var(--font-serif);
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  line-height: 1.15;
  color: var(--ink);
  margin: 12px 0 16px;
}
.recipe-sub {
  font-size: 1.2rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  max-width: 800px;
}
.recipe-meta-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 24px;
  padding: 16px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin: 24px 0;
  font-size: 0.9rem;
}
.meta-item { display: flex; flex-direction: column; }
.meta-label { font-size: 0.72rem; text-transform: uppercase; color: var(--ink-muted); font-weight: 700; letter-spacing: 0.05em; }
.meta-val { font-size: 1.05rem; font-weight: 700; color: var(--ink); }

/* Recipe Media Showcase */
.recipe-media-wrap {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 32px;
  margin-bottom: 40px;
}
@media (max-width: 860px) {
  .recipe-media-wrap { grid-template-columns: 1fr; }
}
.hero-visual-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.pin-preview-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}
.pin-preview-box img {
  border-radius: 10px;
  box-shadow: var(--shadow-md);
  margin-bottom: 14px;
}
.pin-share-btn {
  display: block;
  background: #E60023;
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 10px 16px;
  border-radius: 6px;
  transition: opacity 0.2s;
}
.pin-share-btn:hover { opacity: 0.9; }

/* Interactive Recipe Box */
.recipe-card-box {
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  margin: 40px 0;
  box-shadow: var(--shadow-sm);
}
.recipe-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
}
.scaler-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  font-weight: 600;
}
.scaler-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  cursor: pointer;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.scaler-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.action-btns {
  display: flex;
  gap: 10px;
}
.print-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-alt);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
}

/* Ingredients & Steps */
.ingredients-list {
  list-style: none;
  margin-bottom: 32px;
}
.ing-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #F0ECE1;
  font-size: 0.95rem;
}
.ing-checkbox {
  margin-top: 5px;
  cursor: pointer;
  accent-color: var(--accent);
}
.ing-checked {
  text-decoration: line-through;
  color: var(--ink-muted);
}
.amazon-pantry-link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: underline;
}

.instructions-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.step-item {
  display: flex;
  gap: 18px;
}
.step-num {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.step-body h4 {
  font-size: 1.05rem;
  margin-bottom: 6px;
}
.step-body p {
  color: var(--ink-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Affiliate Tools Callout Box inside Recipe */
.recipe-tools-box {
  background: #FFF9E6;
  border: 1px solid #FFE082;
  border-left: 5px solid var(--amazon-orange);
  border-radius: 10px;
  padding: 24px;
  margin: 36px 0;
}
.tools-box-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #8C5300;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.tools-inline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

/* Nutrition Table */
.nutrition-panel {
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-top: 36px;
}
.nutrition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 16px;
  text-align: center;
  margin-top: 14px;
}
.nutri-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
}
.nutri-val { font-size: 1.25rem; font-weight: 700; color: var(--accent); }
.nutri-label { font-size: 0.72rem; text-transform: uppercase; color: var(--ink-muted); font-weight: 700; }

/* Site Footer & Disclosure */
.site-footer {
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 60px 0 30px;
  margin-top: 60px;
}
.footer-disclosure {
  background: #F4F1EA;
  border-left: 4px solid var(--gold);
  padding: 14px 18px;
  font-size: 0.8rem;
  color: var(--ink-secondary);
  border-radius: 4px;
  margin-bottom: 30px;
}
.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 0.85rem;
  color: var(--ink-muted);
}

/* Print Stylesheet */
@media print {
  .site-header, .site-footer, .filter-bar, .action-btns, .pin-preview-box, .amazon-showcase, .recipe-tools-box, .breadcrumbs {
    display: none !important;
  }
  body, .container, .recipe-card-box {
    background: #fff !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
  }
  .recipe-header h1 { font-size: 24pt !important; }
}
"""

def generate_recipe_schema(recipe, config):
    domain = config["domain"]
    slug = recipe["id"]
    recipe_url = f"{domain}/recipes/{slug}.html"
    pin_url = f"{domain}/assets/pins/pin-{slug}.png"

    ingredients = []
    for ing in recipe.get("ingredients", []):
        text = f"{ing.get('amount', '')} {ing.get('unit', '')} {ing.get('item', '')}"
        if ing.get("notes"):
            text += f" ({ing['notes']})"
        ingredients.append(text.strip())

    steps = []
    for s in recipe.get("instructions", []):
        steps.append({
            "@type": "HowToStep",
            "text": s.get("text", ""),
            "name": s.get("title", f"Step {s.get('step', 1)}")
        })

    schema = {
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "name": recipe["title"],
        "image": [pin_url],
        "description": recipe.get("headline", recipe["title"]),
        "keywords": ", ".join(recipe.get("tags", [])),
        "author": {
            "@type": "Person",
            "name": config["author"]["name"]
        },
        "datePublished": "2026-11-18",
        "prepTime": f"PT{recipe.get('prep_time', 10)}M",
        "cookTime": f"PT{recipe.get('cook_time', 10)}M",
        "totalTime": f"PT{recipe.get('total_time', 20)}M",
        "recipeCategory": recipe.get("category", "Dinner"),
        "recipeCuisine": recipe.get("cuisine", "American"),
        "recipeYield": f"{recipe.get('servings', 4)} servings",
        "nutrition": {
            "@type": "NutritionInformation",
            "calories": f"{recipe.get('calories', 400)} calories",
            "proteinContent": f"{recipe.get('protein', 30)} g",
            "carbohydrateContent": f"{recipe.get('carbs', 20)} g",
            "fatContent": f"{recipe.get('fat', 15)} g",
            "fiberContent": f"{recipe.get('fiber', 4)} g"
        },
        "recipeIngredient": ingredients,
        "recipeInstructions": steps,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "84"
        }
    }
    return json.dumps(schema, indent=2)

def build_recipe_page(recipe, config, all_recipes):
    slug = recipe["id"]
    domain = config["domain"]
    recipe_url = f"{domain}/recipes/{slug}.html"
    pin_url = f"{domain}/assets/pins/pin-{slug}.png"
    schema_json = generate_recipe_schema(recipe, config)

    # Ingredients HTML
    ing_html = ""
    for idx, ing in enumerate(recipe.get("ingredients", [])):
        amt = ing.get("amount", "")
        unit = ing.get("unit", "")
        item = ing.get("item", "")
        notes = f" <em>({ing['notes']})</em>" if ing.get("notes") else ""
        
        # Amazon Affiliate link if mapped
        if ing.get("amazon_key") and ing["amazon_key"] in config["amazon"]["pantry_catalog"]:
            pantry_item = config["amazon"]["pantry_catalog"][ing["amazon_key"]]
            item_display = f"<a href='{pantry_item['url']}' target='_blank' rel='sponsored nofollow noopener' class='amazon-pantry-link'>{item} ↗</a>"
        else:
            item_display = item

        ing_html += f"""
        <li class="ing-item" data-base-amt="{amt}">
          <input type="checkbox" id="ing-{idx}" class="ing-checkbox" onchange="toggleIng(this)">
          <label for="ing-{idx}"><span class="ing-amt">{amt}</span> <span class="ing-unit">{unit}</span> {item_display}{notes}</label>
        </li>
        """

    # Instructions HTML
    steps_html = ""
    for s in recipe.get("instructions", []):
        steps_html += f"""
        <div class="step-item">
          <div class="step-num">{s.get('step', 1)}</div>
          <div class="step-body">
            <h4>{s.get('title', '')}</h4>
            <p>{s.get('text', '')}</p>
          </div>
        </div>
        """

    # Tools Box HTML
    tools_html = ""
    for t_key in recipe.get("recommended_tools", []):
        if t_key in config["amazon"]["tools_catalog"]:
            tool = config["amazon"]["tools_catalog"][t_key]
            tools_html += f"""
            <div class="tool-card">
              <span class="tool-badge">{tool['badge']}</span>
              <div class="tool-title">{tool['name']}</div>
              <div class="tool-desc">{tool['description']}</div>
              <a href="{tool['url']}" target="_blank" rel="sponsored nofollow noopener" class="amazon-btn">
                <span>View on Amazon</span> →
              </a>
            </div>
            """

    # Related Recipes
    related = [r for r in all_recipes if r["id"] != slug][:3]
    related_html = ""
    for r in related:
        related_html += f"""
        <a href="/recipes/{r['id']}.html" class="recipe-card">
          <div class="card-media">
            <img src="/assets/pins/pin-{r['id']}.png" alt="{r['title']}" loading="lazy">
            <span class="card-badge-top">{r['category']}</span>
            <span class="card-time">⏱️ {r['total_time']} mins</span>
          </div>
          <div class="card-body">
            <div class="card-title">{r['title']}</div>
            <div class="card-macros">
              <span><b>{r['protein']}g</b> Protein</span>
              <span><b>{r['calories']}</b> Cals</span>
            </div>
          </div>
        </a>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{recipe['title']} | {config['site_name']}</title>
  <meta name="description" content="{recipe['headline']}">
  <link rel="canonical" href="{recipe_url}">
  
  <!-- OpenGraph / Social -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{recipe['title']} | {config['site_name']}">
  <meta property="og:description" content="{recipe['headline']}">
  <meta property="og:url" content="{recipe_url}">
  <meta property="og:image" content="{pin_url}">
  
  <!-- Pinterest Rich Pin -->
  <meta property="pinterest:pin_image" content="{pin_url}">
  <meta property="pinterest:board" content="{config['pinterest']['board_name']}">
  
  <style>{BASE_CSS}</style>
  
  <!-- Google Recipe Schema JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand">Pure<span>Plated</span></a>
      <nav class="nav-links">
        <a href="/">Recipes</a>
        <a href="/#tools">Kitchen Tools</a>
        <a href="/#about">About</a>
        <a href="/" class="nav-cta">Daily Meal Plan</a>
      </nav>
    </div>
  </header>

  <main class="container recipe-page">
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <span>{recipe.get('category', 'Recipes')}</span> &gt; <span>{recipe['title']}</span>
    </div>

    <!-- Recipe Header -->
    <header class="recipe-header">
      <span class="hero-tag">{recipe.get('category', 'Healthy Meals')}</span>
      <h1>{recipe['title']}</h1>
      <p class="recipe-sub">{recipe.get('headline', '')}</p>
      
      <div class="recipe-meta-bar">
        <div class="meta-item">
          <span class="meta-label">Prep Time</span>
          <span class="meta-val">{recipe.get('prep_time', 10)} mins</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Cook Time</span>
          <span class="meta-val">{recipe.get('cook_time', 10)} mins</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Total Time</span>
          <span class="meta-val">{recipe.get('total_time', 20)} mins</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Protein</span>
          <span class="meta-val">{recipe.get('protein', 30)}g</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Calories</span>
          <span class="meta-val">{recipe.get('calories', 400)} kcal</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Servings</span>
          <span class="meta-val" id="servings-display">{recipe.get('servings', 2)}</span>
        </div>
      </div>
    </header>

    <!-- Visual Showcase & Pinterest Pin Block -->
    <div class="recipe-media-wrap">
      <div class="hero-visual-card">
        <div style="padding:32px; background:var(--surface);">
          <h3 style="font-family:var(--font-serif); margin-bottom:12px; color:var(--accent);">Why This Recipe Works</h3>
          <p style="margin-bottom:16px; color:var(--ink-secondary); line-height:1.6;">{recipe.get('description', '')}</p>
          <ul style="padding-left:20px; color:var(--ink-secondary); line-height:1.7;">
            {''.join(f"<li>{point}</li>" for point in recipe.get('why_it_works', []))}
          </ul>
        </div>
      </div>
      <div class="pin-preview-box">
        <img src="/assets/pins/pin-{slug}.png" alt="Pinterest Pin for {recipe['title']}" width="300" height="450">
        <a href="https://pinterest.com/pin/create/button/?url={recipe_url}&media={pin_url}&description={recipe.get('pin_copy', {}).get('description', '')}" target="_blank" rel="noopener" class="pin-share-btn">
          📌 Save Pin to Pinterest
        </a>
      </div>
    </div>

    <!-- Interactive Recipe Card -->
    <div class="recipe-card-box" id="recipe">
      <div class="recipe-card-header">
        <div>
          <h2 style="font-family:var(--font-serif); color:var(--ink);">{recipe['title']}</h2>
          <span style="font-size:0.85rem; color:var(--ink-muted);">Check items as you shop or cook</span>
        </div>
        <div class="scaler-wrap">
          <span>Servings:</span>
          <button class="scaler-btn active" onclick="scaleServings(this, {recipe.get('servings', 2)}, {recipe.get('servings', 2)})">{recipe.get('servings', 2)}</button>
          <button class="scaler-btn" onclick="scaleServings(this, {recipe.get('servings', 2)}, {recipe.get('servings', 2) * 2})">{recipe.get('servings', 2) * 2}</button>
          <button class="scaler-btn" onclick="scaleServings(this, {recipe.get('servings', 2)}, {recipe.get('servings', 2) * 3})">{recipe.get('servings', 2) * 3}</button>
        </div>
        <div class="action-btns">
          <button class="print-btn" onclick="window.print()">🖨️ Print Recipe</button>
        </div>
      </div>

      <!-- Ingredients Section -->
      <h3 style="margin-bottom:16px; font-family:var(--font-serif);">Ingredients</h3>
      <ul class="ingredients-list">
        {ing_html}
      </ul>

      <!-- Amazon Tools in Recipe Callout -->
      <div class="recipe-tools-box">
        <div class="tools-box-title">
          <span>🔪 Kitchen Equipment Used in This Recipe</span>
        </div>
        <div class="tools-inline-grid">
          {tools_html}
        </div>
      </div>

      <!-- Steps Section -->
      <h3 style="margin:28px 0 16px; font-family:var(--font-serif);">Step-by-Step Instructions</h3>
      <div class="instructions-list">
        {steps_html}
      </div>

      <!-- Chef Pro Tips -->
      <div style="background:var(--accent-light); border-left:4px solid var(--accent); padding:20px; border-radius:8px; margin-top:32px;">
        <h4 style="color:var(--accent); margin-bottom:8px;">💡 Chef's Secret Tips</h4>
        <ul style="padding-left:18px; color:var(--ink); font-size:0.92rem; line-height:1.6;">
          {''.join(f"<li>{tip}</li>" for tip in recipe.get('chef_tips', []))}
        </ul>
      </div>

      <!-- Nutrition Facts Panel -->
      <div class="nutrition-panel">
        <h4 style="font-family:var(--font-serif);">Nutrition Facts (Per Serving)</h4>
        <div class="nutrition-grid">
          <div class="nutri-box"><div class="nutri-val">{recipe.get('calories', 0)}</div><div class="nutri-label">Calories</div></div>
          <div class="nutri-box"><div class="nutri-val">{recipe.get('protein', 0)}g</div><div class="nutri-label">Protein</div></div>
          <div class="nutri-box"><div class="nutri-val">{recipe.get('carbs', 0)}g</div><div class="nutri-label">Carbs</div></div>
          <div class="nutri-box"><div class="nutri-val">{recipe.get('fat', 0)}g</div><div class="nutri-label">Fat</div></div>
          <div class="nutri-box"><div class="nutri-val">{recipe.get('fiber', 0)}g</div><div class="nutri-label">Fiber</div></div>
        </div>
      </div>
    </div>

    <!-- Related Recipes -->
    <div style="margin-top:60px;">
      <h3 style="font-family:var(--font-serif); margin-bottom:24px;">You May Also Like</h3>
      <div class="recipes-grid">
        {related_html}
      </div>
    </div>
  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-disclosure">
        <b>Amazon Affiliate Disclosure:</b> {config['amazon']['disclosure']}
      </div>
      <div class="footer-bottom">
        <div>© 2026 {config['site_name']} • All Rights Reserved. Clean & Easy Daily Meals.</div>
        <div>
          <a href="/feed/pinterest.xml" style="color:var(--gold);">Pinterest Media Feed</a> • 
          <a href="/sitemap.xml">Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    function toggleIng(checkbox) {{
      const label = checkbox.nextElementSibling;
      if (checkbox.checked) {{
        label.classList.add('ing-checked');
      }} else {{
        label.classList.remove('ing-checked');
      }}
    }}

    function scaleServings(btn, baseServings, targetServings) {{
      document.querySelectorAll('.scaler-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('servings-display').innerText = targetServings;
      
      const ratio = targetServings / baseServings;
      document.querySelectorAll('.ing-item').forEach(li => {{
        const baseAmt = parseFloat(li.getAttribute('data-base-amt'));
        if (!isNaN(baseAmt)) {{
          const newAmt = Math.round((baseAmt * ratio) * 100) / 100;
          li.querySelector('.ing-amt').innerText = newAmt;
        }}
      }});
    }}
  </script>
</body>
</html>
"""
    out_file = os.path.join(RECIPES_DIR, f"{slug}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    return out_file

def build_homepage(recipes, config):
    categories = sorted(list(set(r.get("category", "Healthy Meals") for r in recipes)))

    # Recipe Cards HTML
    cards_html = ""
    for r in recipes:
        cards_html += f"""
        <a href="/recipes/{r['id']}.html" class="recipe-card" data-category="{r.get('category', '')}">
          <div class="card-media">
            <img src="/assets/pins/pin-{r['id']}.png" alt="{r['title']}" loading="lazy">
            <span class="card-badge-top">{r['category']}</span>
            <span class="card-time">⏱️ {r['total_time']} mins</span>
          </div>
          <div class="card-body">
            <span class="card-category">{r.get('cuisine', 'Wholesome')}</span>
            <h3 class="card-title">{r['title']}</h3>
            <p class="card-desc">{r.get('headline', '')}</p>
            <div class="card-macros">
              <span><b>{r['protein']}g</b> Protein</span>
              <span><b>{r['calories']}</b> Cals</span>
              <span><b>{r['carbs']}g</b> Carbs</span>
            </div>
          </div>
        </a>
        """

    # Tools Showcase HTML
    tools_html = ""
    for k, tool in config["amazon"]["tools_catalog"].items():
        tools_html += f"""
        <div class="tool-card">
          <span class="tool-badge">{tool['badge']}</span>
          <div class="tool-title">{tool['name']}</div>
          <div class="tool-desc">{tool['description']}</div>
          <a href="{tool['url']}" target="_blank" rel="sponsored nofollow noopener" class="amazon-btn">
            <span>View on Amazon ({tool['price_approx']})</span> →
          </a>
        </div>
        """

    # Category Filter Pills
    filter_html = '<button class="filter-btn active" onclick="filterCategory(\'all\', this)">All Recipes</button>'
    for c in categories:
        filter_html += f'<button class="filter-btn" onclick="filterCategory(\'{c}\', this)">{c}</button>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{config['site_name']} | {config['tagline']}</title>
  <meta name="description" content="{config['description']}">
  <link rel="canonical" href="{config['domain']}/">
  <style>{BASE_CSS}</style>
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand">Pure<span>Plated</span></a>
      <nav class="nav-links">
        <a href="#recipes">Recipes</a>
        <a href="#tools">Essential Tools</a>
        <a href="#about">About</a>
        <a href="#recipes" class="nav-cta">Browse 20-Min Meals</a>
      </nav>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <span class="hero-tag">Daily Clean Eating Made Effortless</span>
      <h1>Healthy, Easy & High-Protein Meals in 25 Minutes or Less</h1>
      <p>{config['description']}</p>
      <div style="display:flex; justify-content:center; gap:16px;">
        <a href="#recipes" class="nav-cta" style="padding:12px 28px; font-size:1.05rem;">Explore Recipes Today →</a>
      </div>
    </div>
  </section>

  <!-- Recipe Catalogue -->
  <main class="container" id="recipes" style="padding-top:40px;">
    <!-- Filter Pills -->
    <div class="filter-bar">
      {filter_html}
    </div>

    <!-- Recipe Cards Grid -->
    <div class="recipes-grid" id="recipes-container">
      {cards_html}
    </div>

    <!-- Amazon Tools Showcase -->
    <section class="amazon-showcase" id="tools">
      <div class="showcase-header">
        <span class="hero-tag">Tested & Trusted Gear</span>
        <h2>Kitchen Tools That Make Healthy Cooking 10x Faster</h2>
        <p>The exact appliances and prep gadgets we rely on daily for effortless, high-protein cooking.</p>
      </div>
      <div class="tools-grid">
        {tools_html}
      </div>
    </section>

    <!-- Editorial Trust & About -->
    <section id="about" style="background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:48px 40px; margin:40px 0;">
      <div style="max-width:760px; margin:0 auto; text-align:center;">
        <span class="hero-tag">Our Culinary Philosophy</span>
        <h2 style="font-family:var(--font-serif); margin-bottom:16px;">High-Protein. Clean Ingredients. Zero Stress.</h2>
        <p style="color:var(--ink-secondary); font-size:1.05rem; line-height:1.7; margin-bottom:24px;">
          Healthy home cooking shouldn't mean spending 90 minutes over a hot stove or buying 30 exotic ingredients. 
          At PurePlated, every single recipe is engineered for <b>maximum protein density</b>, <b>minimal pan cleanup</b>, 
          and ready in <b>under 25 minutes</b>. We prioritize wild-caught seafood, lean poultry, fresh vegetables, 
          and cold-pressed oils.
        </p>
      </div>
    </section>
  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-disclosure">
        <b>Amazon Affiliate Disclosure:</b> {config['amazon']['disclosure']}
      </div>
      <div class="footer-bottom">
        <div>© 2026 {config['site_name']} • Clean & Healthy Meals for Real Life.</div>
        <div>
          <a href="/feed/pinterest.xml" style="color:var(--gold);">Pinterest Media Feed</a> • 
          <a href="/sitemap.xml">Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    function filterCategory(cat, btn) {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      const cards = document.querySelectorAll('.recipe-card');
      cards.forEach(card => {{
        if (cat === 'all' || card.getAttribute('data-category') === cat) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
"""
    out_file = os.path.join(PUBLIC_DIR, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    return out_file

def build_sitemap(recipes, config):
    domain = config["domain"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Homepage
    xml.append(f"""  <url>
    <loc>{domain}/</loc>
    <lastmod>2026-11-18</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

    # Recipes
    for r in recipes:
        xml.append(f"""  <url>
    <loc>{domain}/recipes/{r['id']}.html</loc>
    <lastmod>2026-11-18</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    xml.append('</urlset>')
    sitemap_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    return sitemap_path

def build_pinterest_feed(recipes, config):
    domain = config["domain"]
    board_name = config["pinterest"]["board_name"]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">')
    xml.append('  <channel>')
    xml.append(f'    <title>{escape(config["site_name"])} - Pinterest Recipe Media Feed</title>')
    xml.append(f'    <link>{domain}</link>')
    xml.append(f'    <description>{escape("Daily High-Protein, Healthy & Easy Meal Pins")}</description>')
    xml.append(f'    <language>en-us</language>')

    for idx, r in enumerate(recipes):
        pin_copy = r.get("pin_copy", {})
        title = pin_copy.get("title", r["title"])
        desc = pin_copy.get("description", r["headline"])
        pin_url = f"{domain}/assets/pins/pin-{r['id']}.png"
        link = f"{domain}/recipes/{r['id']}.html?utm_source=pinterest&utm_medium=pin&utm_campaign={r['id']}"

        xml.append('    <item>')
        xml.append(f'      <title>{escape(title)}</title>')
        xml.append(f'      <link>{escape(link)}</link>')
        xml.append(f'      <guid>{escape(r["id"])}</guid>')
        xml.append(f'      <pubDate>Wed, 18 Nov 2026 {12+idx:02d}:00:00 +0000</pubDate>')
        xml.append(f'      <description>{escape(desc)}</description>')
        xml.append(f'      <enclosure url="{escape(pin_url)}" type="image/png" length="85000" />')
        xml.append(f'      <media:content url="{escape(pin_url)}" type="image/png" medium="image" />')
        xml.append(f'      <category>{escape(r.get("category", board_name))}</category>')
        xml.append('    </item>')

    xml.append('  </channel>')
    xml.append('</rss>')

    feed_path = os.path.join(FEED_DIR, "pinterest.xml")
    os.makedirs(FEED_DIR, exist_ok=True)
    with open(feed_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    return feed_path

def build_all():
    recipes, config = load_data()
    os.makedirs(RECIPES_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    print("\n=======================================================")
    print("      PUREPLATED STATIC SITE BUILDER & COMPILER")
    print("=======================================================")
    
    # 1. Compile Recipes
    for r in recipes:
        out = build_recipe_page(r, config, recipes)
        print(f"[✓] Compiled Recipe Page: /recipes/{r['id']}.html")

    # 2. Compile Homepage
    hp_out = build_homepage(recipes, config)
    print(f"[✓] Compiled Homepage: /index.html ({len(recipes)} recipes showcased)")

    # 3. Compile Sitemap
    sm_out = build_sitemap(recipes, config)
    print(f"[✓] Generated Sitemap: /sitemap.xml")

    # 4. Compile Pinterest RSS Media Feed
    feed_out = build_pinterest_feed(recipes, config)
    print(f"[✓] Generated Pinterest Feed: /feed/pinterest.xml")

    # 5. Robots.txt
    robots_path = os.path.join(PUBLIC_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {config['domain']}/sitemap.xml\n")
    print(f"[✓] Generated robots.txt")

    print("=======================================================")
    print(f"[✓] Site compilation complete! Static files ready in {PUBLIC_DIR}\n")

if __name__ == "__main__":
    build_all()
