# PurePlated — Autonomous Amazon Affiliate & Pinterest Recipe Engine

> **Tagline:** Fast, Wholesome & High-Protein Meals in 25 Minutes or Less  
> **Brand:** PurePlated  
> **Target Audience:** Busy professionals, fitness enthusiasts, and health-conscious families looking for quick weeknight dinners with minimal cleanup.

---

## 1. Executive System Overview

PurePlated is a production-grade, end-to-end autonomous media and affiliate engine designed to drive high-intent organic traffic from **Pinterest** and **Google Search**, monetize via the **Amazon Associates** program, and run completely hands-free on a daily schedule.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PUREPLATED AUTONOMOUS ARCHITECTURE                   │
└────────────────────────────────────────────────────────────────────────┘

  [1. Daily Recipe Synthesizer]
        │
        ├── Ingests macro-balanced ingredients (40g+ protein, < 25 mins)
        ├── Calculates exact nutritional facts (Cals, P/C/F/Fiber)
        └── Maps Amazon Kitchen Equipment & Pantry Staples
        │
        ▼
  [2. Pillow Pinterest Pin Studio]
        │
        ├── Generates 1000x1500 px (2:3 aspect ratio) high-res graphics
        ├── High-contrast editorial typography (DejaVu Serif + Sans)
        ├── Floating Macro & Speed Badges (e.g. 18 Mins, 44g Protein)
        └── Auto-watermarked with PUREPLATED.COM
        │
        ▼
  [3. Static Site Compiler]
        │
        ├── Compiles lightning-fast, zero-dependency responsive HTML pages
        ├── Google Recipe JSON-LD schema (Rich Results & Star Ratings)
        ├── Interactive Serving Scaler (2, 4, 6 servings) & Checklists
        ├── Amazon Affiliate Product Showcase Boxes (Prime & Best Sellers)
        ├── Updates sitemap.xml, robots.txt, and /feed/pinterest.xml
        └── Generates 7-Day Interactive Meal Planner (/meal-planner.html)
        │
        ▼
  [4. Autonomous Traffic Syndication]
        │
        ├── Make.com Scenario (ID: 7094447) with builtin:Break auto-retry
        ├── Reads /feed/pinterest.xml media enclosures & descriptions
        └── Auto-publishes to Pinterest twice daily (8:00 AM & 5:00 PM EST)
```

---

## 2. Amazon Affiliate Monetization Blueprint

### A. Contextual Kitchen Equipment ("Tools We Used" Box)
Embedded directly inside every recipe page, featuring high-converting kitchen gadgets with verified customer reviews and high cart values:
* **Air Fryers:** Ninja AF101 4-Qt (`$89.99`)
* **High-Speed Blenders:** NutriBullet Pro 900W (`$79.99`)
* **Digital Food Scales:** GreaterGoods Precision Gram Scale (`$14.99`)
* **Glass Meal Prep Containers:** Prep Naturals 5-Pack Airtight Glass (`$29.99`)
* **Chef Knives:** Victorinox Fibrox Pro 8" Swiss High-Carbon (`$44.95`)
* **Meat Thermometers:** ThermoPro TP19H Waterproof Digital Instant Read (`$17.99`)
* **Cast Iron Cookware:** Lodge 10.25" Pre-Seasoned Skillet (`$19.90`)
* **Vegetable Choppers:** Fullstar 4-in-1 Veggie Dicer & Spiralizer (`$24.99`)

### B. Inline Pantry Essentials Links
Ingredients within the recipe checklist include contextual affiliate text links:
* California Olive Ranch 100% Extra Virgin Olive Oil
* Chosen Foods High Smoke Point Avocado Oil Spray
* Redmond Real Ancient Fine Sea Salt
* Viva Naturals Organic Raw Chia Seeds
* Banza High-Protein Chickpea Pasta

### C. Legal Compliance & FTC Disclosures
* Standard Amazon Associates disclosure prominently displayed in the footer and directly above all recipe product showcases:
  > *"As an Amazon Associate, PurePlated earns from qualifying purchases at no additional cost to you. We only recommend kitchen equipment and wholesome ingredients we genuinely use and love."*
* Dynamic Amazon tag configuration in `config/site_config.json` (`affiliate_tag: "pureplated-20"`).

---

## 3. Pinterest Traffic Engine & Automation

### A. Graphic Specifications
* **Dimensions:** Exact 1000 x 1500 px (Pinterest 2:3 vertical aspect ratio).
* **Typography:** Layered editorial hierarchy:
  * Eyebrow pill: Category & cook time
  * Title: DejaVu Serif Bold (52pt)
  * Benefit Pills: 4 rounded floating badges (Protein, Calories, Carbs, Total Time)
  * Call To Action: "TAP FOR RECIPE & SHOPPING LIST →"
  * Watermark: `PUREPLATED.COM`

### B. Make.com Scenario Automation
* **Scenario ID:** `7094447` (`PurePlated - Daily Healthy Meals Pinterest Automation`)
* **Dashboard:** [https://us2.make.com/2010020/scenarios/7094447](https://us2.make.com/2010020/scenarios/7094447)
* **Architecture:**
  1. Trigger: `rss:TriggerNewArticle` watching `https://pureplated.com/feed/pinterest.xml`.
  2. Action: `pinterest:createPin` using verified OAuth connection `12397534`.
  3. Resilience: `builtin:Break` error handler with 3 retries at 15-minute intervals. If Pinterest's API has a temporary crawler timeout or code `2787` glitch, Make automatically pauses and retries without failing.

---

## 4. Key CLI Commands & Workflows

### 1. Generate a New Daily Recipe & Pinterest Pin
```bash
python3 src/engine/recipe_generator.py
```
*Synthesizes a new meal, computes macros, generates the 1000x1500 pin, re-compiles the site, and updates the RSS feeds.*

### 2. Render / Regenerate All Pinterest Pins
```bash
python3 src/pinterest/pin_generator.py
```

### 3. Recompile the Static Website
```bash
python3 src/engine/build_site.py
```

### 4. Check / Advance the Pinterest Publishing Queue
```bash
# Check queue status and prior post counts
python3 src/pinterest/publish_pins.py --status

# Dispatch next pin
python3 src/pinterest/publish_pins.py
```

### 5. Run the Master Autonomous Pipeline
```bash
./scripts/daily_pipeline.py
```

---

## 5. Directory Structure

```
daily-healthy-meals/
├── config/
│   ├── site_config.json                     # Site metadata, Amazon catalogs, and tags
│   ├── make_pinterest_scenario_blueprint.json # 100% compliant Make.com blueprint
│   └── systemd/
│       ├── pureplated-daily.service          # Daily cron runner service
│       └── pureplated-daily.timer            # 8:00 AM EST trigger timer
├── public/                                  # Production-ready static web bundle
│   ├── index.html                           # Fast homepage with live filters & search
│   ├── meal-planner.html                    # 7-Day Interactive Meal Planner tool
│   ├── sitemap.xml                          # Google Search Console XML sitemap
│   ├── robots.txt                           # Search engine crawling directives
│   ├── feed/
│   │   └── pinterest.xml                    # RSS 2.0 with media enclosures for Make
│   ├── assets/
│   │   └── pins/                            # High-res 1000x1500 vertical Pinterest pins
│   └── recipes/                             # Full recipe pages with JSON-LD schemas
├── scripts/
│   ├── daily_pipeline.py                    # Master orchestrator script
│   └── deploy_make_scenario.py              # One-click deployer to Make.com
└── src/
    ├── data/
    │   ├── recipes.json                     # Recipe database with full macros & gear
    │   └── pinterest_queue.db               # SQLite rotation state tracker
    ├── engine/
    │   ├── recipe_generator.py              # Autonomous recipe synthesizer
    │   └── build_site.py                    # Static compiler & schema generator
    └── pinterest/
        ├── pin_generator.py                 # Pillow 1000x1500 graphic generator
        └── publish_pins.py                  # Queue dispatcher & API syndicator
```
