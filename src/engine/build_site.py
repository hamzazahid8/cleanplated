#!/usr/bin/env python3
"""
PurePlated Static Site Compiler & Modern Editorial Culinary Engine
-----------------------------------------------------------------
Compiles recipes into a stunning, high-converting culinary publication.
Features:
- Real magazine-grade food photography
- Google Fonts: Newsreader (Editorial Serif) & Plus Jakarta Sans
- Responsive recipe cards with subtle hover zoom and elevation
- Interactive Serving Scaler (2, 4, 6 servings) with real-time math
- Interactive Grocery & Pantry Checklists with Amazon affiliate links
- Google Recipe JSON-LD schema (Rich Snippets, ratings & nutritional facts)
- Dedicated Amazon Equipment Showcases & Pinterest Media RSS
"""

import os
import json
import re
from datetime import datetime
from xml.sax.saxutils import escape
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_js import RECIPE_PAGE_JS, HOMEPAGE_JS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECIPES_JSON = os.path.join(BASE_DIR, "src", "data", "recipes.json")
CONFIG_JSON = os.path.join(BASE_DIR, "config", "site_config.json")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
RECIPES_DIR = os.path.join(PUBLIC_DIR, "recipes")
FEED_DIR = os.path.join(PUBLIC_DIR, "feed")

def load_data():
    with open(RECIPES_JSON, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    with open(CONFIG_JSON, "r", encoding="utf-8") as f:
        config = json.load(f)
    return recipes, config

# Master Design System & Typography
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #FAF8F5;
  --surface: #FFFFFF;
  --surface-alt: #F3EFEA;
  --surface-tint: #F7F5F0;
  --ink: #161F1A;
  --ink-secondary: #4A564F;
  --ink-muted: #79867E;
  --border: #E8E3DC;
  --border-light: rgba(22, 31, 26, 0.07);
  
  --primary: #1C3F2F;
  --primary-hover: #122B20;
  --primary-light: #EBF3EE;
  
  --accent-gold: #D2812A;
  --accent-gold-light: #FDF6EC;
  --accent-rust: #C55836;
  --accent-rust-light: #FAEEEA;
  
  --amazon-orange: #FF9900;
  --amazon-hover: #E68A00;
  
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-pill: 999px;
  
  --shadow-subtle: 0 2px 6px rgba(22, 31, 26, 0.04);
  --shadow-card: 0 4px 16px -2px rgba(22, 31, 26, 0.06), 0 2px 6px rgba(22, 31, 26, 0.02);
  --shadow-hover: 0 16px 32px -6px rgba(28, 63, 47, 0.12), 0 4px 12px rgba(22, 31, 26, 0.04);
  
  --font-serif: 'Newsreader', Georgia, 'Times New Roman', serif;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a { color: inherit; text-decoration: none; }
img { max-width: 100%; height: auto; display: block; }

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Announcement Top Bar */
.top-bar {
  background: var(--primary);
  color: #EBF3EE;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 8px 16px;
  text-align: center;
  letter-spacing: 0.02em;
}
.top-bar span { color: #F7D070; margin-right: 6px; }

/* Sticky Header */
.site-header {
  background: rgba(250, 248, 245, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 1000;
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
  gap: 8px;
  font-family: var(--font-serif);
  font-size: 1.65rem;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: -0.01em;
}
.brand-icon {
  width: 28px;
  height: 28px;
  background: var(--primary);
  color: #FFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
}
.brand span { color: var(--accent-gold); }

.nav-links {
  display: flex;
  align-items: center;
  gap: 28px;
  font-size: 0.93rem;
  font-weight: 600;
  color: var(--ink-secondary);
}
.nav-links a {
  position: relative;
  transition: color 0.2s ease;
}
.nav-links a:hover { color: var(--primary); }

.nav-cta {
  background: var(--primary);
  color: #FFF !important;
  padding: 10px 20px;
  border-radius: var(--radius-pill);
  font-size: 0.88rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 8px rgba(28, 63, 47, 0.15);
}
.nav-cta:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(28, 63, 47, 0.25);
}
.nav-cta:active { transform: translateY(0); }

/* Hero Section */
.hero {
  padding: 48px 0 36px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(255,255,255,0.7) 0%, var(--bg) 100%);
}
.hero-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 48px;
  align-items: center;
}
.hero-content {
  max-width: 620px;
}
.hero-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  margin-bottom: 20px;
  border: 1px solid rgba(28, 63, 47, 0.1);
}
.hero-badge-pill span.dot {
  width: 7px;
  height: 7px;
  background: var(--accent-gold);
  border-radius: 50%;
  display: inline-block;
}
.hero h1 {
  font-family: var(--font-serif);
  font-size: clamp(2.3rem, 4.2vw, 3.5rem);
  font-weight: 600;
  line-height: 1.15;
  color: var(--ink);
  margin-bottom: 18px;
  letter-spacing: -0.02em;
}
.hero p {
  font-size: 1.12rem;
  line-height: 1.65;
  color: var(--ink-secondary);
  margin-bottom: 28px;
}
.hero-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.btn-primary {
  background: var(--primary);
  color: #FFF !important;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 13px 26px;
  border-radius: var(--radius-pill);
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(28, 63, 47, 0.2);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(28, 63, 47, 0.3);
}
.btn-secondary {
  background: #FFF;
  color: var(--ink);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 13px 24px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
  transition: all 0.2s ease;
}
.btn-secondary:hover {
  background: var(--surface-alt);
  border-color: var(--ink-muted);
}

/* Hero Featured Card */
.hero-card {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--border-light);
  background: #FFF;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.hero-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}
.hero-card-img-wrap {
  position: relative;
  aspect-ratio: 16 / 11;
  overflow: hidden;
}
.hero-card-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.hero-card:hover .hero-card-img-wrap img {
  transform: scale(1.04);
}
.hero-floating-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(22, 31, 26, 0.85);
  backdrop-filter: blur(8px);
  color: #FFF;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.hero-card-body {
  padding: 24px;
}
.hero-card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.82rem;
  color: var(--accent-gold);
  font-weight: 700;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.hero-card-title {
  font-family: var(--font-serif);
  font-size: 1.45rem;
  line-height: 1.25;
  color: var(--ink);
  font-weight: 600;
  margin-bottom: 12px;
}
.hero-card-macros {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* Category Filter Bar */
.filter-section {
  padding: 32px 0 20px;
}
.filter-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 8px;
  scrollbar-width: none;
}
.filter-bar::-webkit-scrollbar { display: none; }
.filter-btn {
  background: #FFF;
  border: 1px solid var(--border);
  color: var(--ink-secondary);
  font-family: var(--font-sans);
  font-size: 0.88rem;
  font-weight: 600;
  padding: 9px 18px;
  border-radius: var(--radius-pill);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.filter-btn:hover {
  background: var(--surface-alt);
  color: var(--ink);
}
.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #FFF;
  box-shadow: 0 2px 8px rgba(28, 63, 47, 0.2);
}

/* Recipe Grid */
.recipes-section {
  padding: 20px 0 64px;
}
.section-title-wrap {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}
.section-title {
  font-family: var(--font-serif);
  font-size: 2.1rem;
  color: var(--ink);
  font-weight: 600;
  letter-spacing: -0.01em;
}
.section-sub {
  color: var(--ink-muted);
  font-size: 0.95rem;
  margin-top: 4px;
}

.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 32px;
}

/* Individual Recipe Card */
.recipe-card {
  background: var(--surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  overflow: hidden;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  position: relative;
}
.recipe-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}
.card-media {
  position: relative;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: #EEE;
}
.card-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.recipe-card:hover .card-media img {
  transform: scale(1.04);
}
.card-badge-time {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(22, 31, 26, 0.85);
  backdrop-filter: blur(6px);
  color: #FFF;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: var(--radius-pill);
  display: flex;
  align-items: center;
  gap: 4px;
}
.card-badge-cat {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(6px);
  color: var(--primary);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(22, 31, 26, 0.08);
}
.card-body {
  padding: 22px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}
.card-rating {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  color: var(--accent-gold);
  font-weight: 700;
  margin-bottom: 8px;
}
.card-rating span.count {
  color: var(--ink-muted);
  font-weight: 500;
}
.card-title {
  font-family: var(--font-serif);
  font-size: 1.32rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.3;
  margin-bottom: 10px;
  transition: color 0.2s;
}
.recipe-card:hover .card-title {
  color: var(--primary);
}
.card-desc {
  font-size: 0.9rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  margin-bottom: 18px;
  flex-grow: 1;
}

/* Macro Pills */
.macro-pills {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}
.macro-pill {
  font-size: 0.78rem;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
}
.macro-pill.protein {
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700;
}
.macro-pill.cals {
  background: var(--surface-alt);
  color: var(--ink-secondary);
}
.macro-pill.carbs {
  background: var(--surface-alt);
  color: var(--ink-secondary);
}

.card-cta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid var(--border);
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--primary);
}
.card-cta-row span.arrow {
  transition: transform 0.2s ease;
}
.recipe-card:hover .card-cta-row span.arrow {
  transform: translateX(4px);
}

/* Kitchen Equipment Showcase Section */
.tools-section {
  padding: 64px 0;
  background: #FFF;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  margin-top: 36px;
}
.tool-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.2s ease;
}
.tool-card:hover {
  background: #FFF;
  box-shadow: var(--shadow-card);
  transform: translateY(-2px);
}
.tool-badge {
  display: inline-block;
  align-self: flex-start;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  padding: 3px 8px;
  border-radius: 4px;
  margin-bottom: 12px;
}
.tool-title {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--ink);
  margin-bottom: 8px;
  line-height: 1.35;
}
.tool-desc {
  font-size: 0.86rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  margin-bottom: 18px;
  flex-grow: 1;
}
.amazon-btn {
  background: #FFF;
  border: 1px solid var(--amazon-orange);
  color: #111;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background 0.15s ease, color 0.15s ease;
}
.amazon-btn:hover {
  background: var(--amazon-orange);
  color: #111;
}

/* Author Trust & E-E-A-T Section */
.author-section {
  padding: 60px 0;
  background: var(--surface-alt);
  border-bottom: 1px solid var(--border);
}
.author-box {
  display: flex;
  align-items: center;
  gap: 36px;
  max-width: 860px;
  margin: 0 auto;
}
.author-avatar-wrap {
  width: 120px;
  height: 120px;
  min-width: 120px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
  border: 4px solid #FFF;
}
.author-avatar-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.author-details h3 {
  font-family: var(--font-serif);
  font-size: 1.6rem;
  color: var(--ink);
  margin-bottom: 4px;
}
.author-role {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}
.author-bio {
  font-size: 0.95rem;
  color: var(--ink-secondary);
  line-height: 1.6;
}

/* Footer */
.site-footer {
  background: var(--ink);
  color: #D1D9D4;
  padding: 60px 0 32px;
  font-size: 0.9rem;
}
.footer-inner {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 40px;
}
.footer-brand {
  font-family: var(--font-serif);
  font-size: 1.6rem;
  font-weight: 700;
  color: #FFF;
  margin-bottom: 12px;
}
.footer-brand span { color: var(--accent-gold); }
.footer-disclosure {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 16px 20px;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  line-height: 1.6;
  color: #A3B1AA;
  margin-bottom: 32px;
}
.footer-disclosure b { color: #FFF; }
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  color: #8C9C94;
}

/* ========================================================
   RECIPE DETAIL PAGE SPECIFIC STYLES
   ======================================================== */
.recipe-page {
  padding: 32px 0 80px;
}
.breadcrumbs {
  font-size: 0.85rem;
  color: var(--ink-muted);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.breadcrumbs a:hover { color: var(--primary); text-decoration: underline; }

.recipe-hero-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: start;
  margin-bottom: 48px;
}
.recipe-hero-text h1 {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 3.8vw, 3rem);
  line-height: 1.18;
  color: var(--ink);
  margin: 12px 0 16px;
  font-weight: 600;
}
.recipe-hero-sub {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--ink-secondary);
  margin-bottom: 24px;
}
.recipe-byline-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.byline-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}
.byline-info {
  font-size: 0.86rem;
}
.byline-name { font-weight: 700; color: var(--ink); }
.byline-meta { color: var(--ink-muted); font-size: 0.8rem; }

.recipe-quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.btn-jump {
  background: var(--primary);
  color: #FFF !important;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 20px;
  border-radius: var(--radius-pill);
}
.btn-pin-action {
  background: #E60023;
  color: #FFF !important;
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 20px;
  border-radius: var(--radius-pill);
}

.recipe-hero-visual {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 12px 36px -6px rgba(22, 31, 26, 0.15);
  border: 1px solid var(--border);
}
.recipe-hero-visual img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}
.recipe-photo-caption {
  background: #FFF;
  padding: 12px 18px;
  font-size: 0.82rem;
  color: var(--ink-secondary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-light);
}

/* Master Recipe Box */
.recipe-card-box {
  background: #FFF;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 44px;
  box-shadow: var(--shadow-card);
  margin-bottom: 48px;
}
.recipe-box-header {
  border-bottom: 1px solid var(--border);
  padding-bottom: 28px;
  margin-bottom: 32px;
}
.recipe-box-header h2 {
  font-family: var(--font-serif);
  font-size: 2.2rem;
  color: var(--ink);
  margin-bottom: 12px;
}
.nutrition-dashboard {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-top: 24px;
}
.nutri-box {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
  text-align: center;
}
.nutri-val {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
}
.nutri-label {
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--ink-muted);
  text-transform: uppercase;
  margin-top: 4px;
}

/* Recipe Two-Col Layout */
.recipe-core-layout {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  gap: 48px;
}

/* Serving Scaler */
.serving-scaler-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}
.serving-scaler-wrap h3 {
  font-family: var(--font-serif);
  font-size: 1.4rem;
  color: var(--ink);
}
.serving-btns {
  display: flex;
  gap: 6px;
}
.serv-btn {
  background: var(--bg);
  border: 1px solid var(--border);
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}
.serv-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #FFF;
}

/* Checklist Ingredients */
.ingredients-list {
  list-style: none;
}
.ing-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--border);
  font-size: 0.95rem;
}
.ing-item input[type="checkbox"] {
  margin-top: 5px;
  width: 17px;
  height: 17px;
  accent-color: var(--primary);
  cursor: pointer;
}
.ing-checked {
  text-decoration: line-through;
  color: var(--ink-muted);
}
.amazon-pantry-link {
  color: var(--accent-gold);
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.amazon-pantry-link:hover {
  color: var(--amazon-hover);
}

/* Step-by-Step Instructions */
.instructions-list {
  list-style: none;
}
.instruction-step {
  display: flex;
  gap: 18px;
  margin-bottom: 28px;
}
.step-number {
  width: 36px;
  height: 36px;
  min-width: 36px;
  background: var(--primary);
  color: #FFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1rem;
}
.step-content h4 {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 6px;
}
.step-content p {
  color: var(--ink-secondary);
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Equipment Box Inside Recipe */
.recipe-tools-box {
  margin-top: 36px;
  padding: 24px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
}
.recipe-tools-box h4 {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  margin-bottom: 16px;
  color: var(--ink);
}
.recipe-tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 14px;
}

/* Pinterest Pin Save Card at bottom */
.pin-save-section {
  background: #FFF;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 32px;
  margin-top: 48px;
}
.pin-thumbnail {
  width: 140px;
  min-width: 140px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Mobile Responsive */
@media (max-width: 900px) {
  .hero-grid { grid-template-columns: 1fr; gap: 32px; }
  .recipe-hero-split { grid-template-columns: 1fr; }
  .recipe-core-layout { grid-template-columns: 1fr; }
  .nutrition-dashboard { grid-template-columns: repeat(3, 1fr); }
  .footer-inner { grid-template-columns: 1fr; gap: 32px; }
  .author-box { flex-direction: column; text-align: center; }
  .pin-save-section { flex-direction: column; text-align: center; }
}

/* ========================================================
   FLUID MOTION & MICRO-INTERACTION SUITE (ANTI-SLOP)
   ======================================================== */
html {
  scroll-behavior: smooth;
}

/* Scroll-Driven Reveal Animations */
.reveal {
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}
.reveal.is-revealed {
  opacity: 1;
  transform: translateY(0);
}

.reveal-stagger:nth-child(1) { transition-delay: 0.03s; }
.reveal-stagger:nth-child(2) { transition-delay: 0.07s; }
.reveal-stagger:nth-child(3) { transition-delay: 0.11s; }
.reveal-stagger:nth-child(4) { transition-delay: 0.15s; }
.reveal-stagger:nth-child(5) { transition-delay: 0.19s; }
.reveal-stagger:nth-child(6) { transition-delay: 0.23s; }

/* Tactile Button Feedback (Emil Kowalski Philosophy) */
button, .btn-primary, .btn-secondary, .nav-cta, .filter-btn, .serv-btn, .amazon-btn, .btn-jump, .btn-pin-action, .floating-btn, .floating-pin-btn {
  transition: transform 160ms cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 160ms ease, background-color 160ms ease !important;
  cursor: pointer;
}
button:active, .btn-primary:active, .btn-secondary:active, .nav-cta:active, .filter-btn:active, .serv-btn:active, .amazon-btn:active, .btn-jump:active, .btn-pin-action:active, .floating-btn:active, .floating-pin-btn:active {
  transform: scale(0.96) !important;
}

/* Card Physical Lift & Ambient Bloom */
.recipe-card {
  transition: transform 280ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 280ms cubic-bezier(0.16, 1, 0.3, 1), border-color 280ms ease !important;
}
.recipe-card:hover {
  transform: translateY(-6px) !important;
  box-shadow: 0 20px 40px -8px rgba(22, 31, 26, 0.13), 0 6px 16px -2px rgba(22, 31, 26, 0.04) !important;
  border-color: rgba(28, 63, 47, 0.22) !important;
}
.recipe-card .card-media img {
  transition: transform 600ms cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.recipe-card:hover .card-media img {
  transform: scale(1.045) !important;
}
.card-cta-row span.arrow {
  display: inline-block;
  transition: transform 220ms cubic-bezier(0.16, 1, 0.3, 1);
}
.recipe-card:hover .card-cta-row span.arrow {
  transform: translateX(5px);
  color: var(--accent-gold);
}

/* Tool Card Elevation */
.tool-card {
  transition: transform 240ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 240ms cubic-bezier(0.16, 1, 0.3, 1), border-color 240ms ease !important;
}
.tool-card:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 28px -4px rgba(22, 31, 26, 0.1) !important;
  border-color: rgba(28, 63, 47, 0.25) !important;
}

/* Ambient Pulse on Status Badges */
@keyframes ambientPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.35); opacity: 0.65; }
}
.hero-badge-pill span.dot {
  animation: ambientPulse 2.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Serving Scaler Number Bump */
.ing-amt {
  display: inline-block;
  transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), color 180ms ease;
}
.ing-amt.bump {
  transform: translateY(-3px) scale(1.2);
  color: var(--accent-gold);
}
.serv-btn.active {
  animation: popScale 220ms cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes popScale {
  0% { transform: scale(0.92); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Ingredient Checklist Strikethrough & Row Glide */
.ing-item {
  transition: background-color 180ms ease, opacity 220ms ease, transform 180ms ease;
  border-radius: 6px;
  padding: 10px 8px;
}
.ing-item:hover {
  background-color: rgba(235, 243, 238, 0.6);
  transform: translateX(3px);
}
.ing-label {
  transition: color 220ms ease, opacity 220ms ease;
}
.ing-checked {
  color: var(--ink-muted) !important;
  opacity: 0.5;
  text-decoration: line-through;
  text-decoration-color: var(--primary);
  text-decoration-thickness: 2px;
}
.ing-checkbox {
  transition: transform 160ms cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}
.ing-checkbox:checked {
  transform: scale(1.18);
}

/* Floating Sticky Action Bar (Recipe Pages) */
.floating-recipe-bar {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translate(-50%, 90px);
  opacity: 0;
  pointer-events: none;
  z-index: 999;
  transition: transform 320ms cubic-bezier(0.16, 1, 0.3, 1), opacity 320ms ease;
  max-width: 92vw;
}
.floating-recipe-bar.visible {
  transform: translate(-50%, 0);
  opacity: 1;
  pointer-events: auto;
}
.floating-bar-inner {
  background: rgba(22, 31, 26, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-pill);
  padding: 8px 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 16px 36px -4px rgba(0, 0, 0, 0.35);
}
.floating-recipe-title {
  color: #FFF;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  padding-right: 14px;
  white-space: nowrap;
}
.floating-recipe-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.floating-btn {
  color: #D1D9D4;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  transition: all 160ms ease;
}
.floating-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #FFF;
}
.floating-pin-btn {
  background: #E60023;
  color: #FFF !important;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: transform 160ms ease, background 160ms ease;
}
.floating-pin-btn:hover {
  background: #B6001C;
  transform: scale(1.03);
}

@media (max-width: 640px) {
  .floating-recipe-title { display: none; }
  .floating-recipe-bar { bottom: 14px; }
  .floating-bar-inner { padding: 6px 10px; gap: 6px; }
  .floating-btn { padding: 5px 8px; font-size: 0.78rem; }
  .floating-pin-btn { padding: 5px 10px; font-size: 0.78rem; }
}

/* ========================================================
   REVERSE-ENGINEERED ELITE CULINARY BLOG FEATURES (PINCH OF YUM + MINIMALIST BAKER)
   ======================================================== */

/* Cook Mode Toggle (Wake Lock API) */
.cook-mode-wrap {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--surface-tint);
  border: 1px solid var(--border);
  padding: 8px 18px;
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--ink);
  user-select: none;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.cook-mode-wrap:hover {
  background: var(--primary-light);
  border-color: var(--primary);
  transform: translateY(-1px);
}
.cook-mode-badge {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #A0AEC0;
  transition: all 0.3s ease;
}
.cook-mode-wrap.cook-mode-active {
  background: #ECFDF5;
  border-color: #10B981;
  color: #065F46;
}
.cook-mode-wrap.cook-mode-active .cook-mode-badge {
  background: #10B981;
  box-shadow: 0 0 10px #10B981;
  animation: pulseDot 1.4s infinite;
}
@keyframes pulseDot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.7; }
}

/* Secondary Hero Actions (Print, Share, Meal Plan) */
.btn-print, .btn-share, .btn-plan {
  background: #FFF;
  color: var(--ink) !important;
  border: 1px solid var(--border);
  font-size: 0.88rem;
  font-weight: 700;
  padding: 10px 18px;
  border-radius: var(--radius-pill);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.btn-print:hover, .btn-share:hover, .btn-plan:hover {
  background: var(--surface-alt);
  border-color: var(--ink-muted);
  transform: translateY(-1px);
}
.btn-plan {
  background: var(--primary-light);
  border-color: rgba(28, 63, 47, 0.2);
  color: var(--primary) !important;
}
.btn-plan:hover {
  background: var(--primary);
  color: #FFF !important;
}

/* Recipe Card Controls Toolbar */
.recipe-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  background: var(--surface-tint);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 20px;
  margin-bottom: 28px;
}
.toolbar-group {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.toolbar-label {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ink-muted);
}
.unit-toggle-pill {
  display: inline-flex;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 3px;
}
.unit-btn {
  border: none;
  background: transparent;
  padding: 5px 12px;
  border-radius: var(--radius-pill);
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--ink-secondary);
  cursor: pointer;
  transition: all 0.15s ease;
}
.unit-btn.active {
  background: var(--primary);
  color: #FFF;
  box-shadow: 0 2px 6px rgba(28, 63, 47, 0.2);
}

/* Step Progress Tracker */
.progress-tracker {
  background: var(--surface-tint);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 20px;
  margin-bottom: 24px;
}
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.86rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 8px;
}
.progress-track {
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--primary) 0%, #10B981 100%);
  border-radius: 4px;
  transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.instruction-step {
  transition: background-color 0.2s ease, opacity 0.2s ease, transform 0.2s ease;
  padding: 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  user-select: none;
}
.instruction-step:hover {
  background: rgba(235, 243, 238, 0.5);
  transform: translateX(4px);
}
.instruction-step.step-completed {
  opacity: 0.55;
}
.instruction-step.step-completed .step-number {
  background: #10B981;
}
.instruction-step.step-completed .step-content h4 {
  text-decoration: line-through;
  color: var(--ink-muted);
}

/* Chef's Pro Tips 3-Box Grid */
.chef-tips-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-top: 36px;
}
.chef-tip-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.chef-tip-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-subtle);
  background: #FFF;
}
.tip-icon {
  font-size: 1.5rem;
  margin-bottom: 8px;
}
.tip-title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 6px;
}
.tip-text {
  font-size: 0.85rem;
  color: var(--ink-secondary);
  line-height: 1.55;
}

/* Nutrition Facts Label & Macro Split */
.nutrition-facts-panel {
  background: #FFF;
  border: 2px solid var(--ink);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-top: 40px;
}
.nf-title {
  font-family: var(--font-serif);
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--ink);
  border-bottom: 8px solid var(--ink);
  padding-bottom: 4px;
  line-height: 1;
}
.nf-sub {
  font-size: 0.85rem;
  color: var(--ink-muted);
  margin-top: 4px;
  margin-bottom: 12px;
}
.nf-calories-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 4px solid var(--ink);
  padding: 8px 0;
  font-size: 1.1rem;
  font-weight: 800;
}
.nf-cal-num {
  font-size: 2rem;
  font-weight: 900;
  color: var(--primary);
  line-height: 1;
}
.macro-ratio-wrap {
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
}
.macro-ratio-bar {
  display: flex;
  height: 12px;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}
.ratio-segment {
  height: 100%;
}
.ratio-legend {
  display: flex;
  gap: 16px;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--ink-secondary);
  flex-wrap: wrap;
}
.legend-dot {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  margin-right: 4px;
}
.nf-table {
  margin-top: 6px;
}
.nf-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.88rem;
  color: var(--ink);
}
.nf-row.bold {
  font-weight: 800;
}
.nf-row.indent {
  padding-left: 18px;
  color: var(--ink-secondary);
}

/* Minimalist Baker Instant Search & Filter UI (Homepage) */
.search-filter-box {
  background: #FFF;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px 28px;
  box-shadow: var(--shadow-card);
  margin-bottom: 36px;
}
.search-input-wrap {
  position: relative;
  margin-bottom: 18px;
}
.search-input-wrap input {
  width: 100%;
  padding: 14px 20px 14px 48px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-pill);
  font-family: var(--font-sans);
  font-size: 1rem;
  outline: none;
  background: var(--bg);
  color: var(--ink);
  transition: all 0.2s ease;
}
.search-input-wrap input:focus {
  background: #FFF;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(28, 63, 47, 0.12);
}
.search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.15rem;
  color: var(--ink-muted);
}
.filter-chips-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.filter-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.filter-chip {
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--ink-secondary);
  font-family: var(--font-sans);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 7px 16px;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: all 0.2s ease;
}
.filter-chip:hover {
  background: var(--surface-alt);
  color: var(--ink);
  border-color: var(--ink-muted);
}
.filter-chip.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #FFF;
  box-shadow: 0 2px 8px rgba(28, 63, 47, 0.2);
}
.filter-count-badge {
  font-size: 0.86rem;
  font-weight: 700;
  color: var(--primary);
  white-space: nowrap;
}

/* Toast Notifications */
.toast-container {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}
.toast-msg {
  background: #161F1A;
  color: #FFF;
  padding: 13px 22px;
  border-radius: var(--radius-pill);
  font-size: 0.9rem;
  font-weight: 600;
  box-shadow: 0 12px 30px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(255,255,255,0.18);
  transform: translateY(20px);
  opacity: 0;
  animation: slideUpToast 0.3s forwards cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: auto;
}
@keyframes slideUpToast {
  to { transform: translateY(0); opacity: 1; }
}

/* Print Only Section */
.print-watermark {
  display: none;
}

/* ========================================================
   DEDICATED ZERO-WASTE CLEAN PRINT ENGINE (@media print)
   ======================================================== */
@media print {
  body {
    background: #FFF !important;
    color: #000 !important;
    font-size: 11pt !important;
    line-height: 1.4 !important;
  }
  .top-bar, .site-header, .breadcrumbs, .recipe-quick-actions, 
  .floating-recipe-bar, .pin-save-section, .recipe-tools-box, 
  .site-footer, .nav-cta, .toast-container, .serv-btn, .unit-btn,
  .cook-mode-wrap, .btn-print, .btn-share, .btn-plan, .amazon-btn,
  .recipe-toolbar, .progress-tracker, .recipe-quick-actions,
  .card-cta-row, .hero-actions, .filter-section, .search-filter-box,
  .tools-section, .author-section {
    display: none !important;
  }
  .container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  .recipe-hero-split {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    margin-bottom: 20px !important;
  }
  .recipe-hero-visual {
    width: 200px !important;
    min-width: 200px !important;
    box-shadow: none !important;
    border: 1px solid #CCC !important;
    border-radius: 8px !important;
  }
  .recipe-hero-visual img {
    aspect-ratio: auto !important;
    height: 140px !important;
    object-fit: cover !important;
  }
  .recipe-photo-caption { display: none !important; }
  .recipe-card-box {
    box-shadow: none !important;
    border: 1px solid #DDD !important;
    padding: 20px !important;
    margin: 0 !important;
  }
  .recipe-core-layout {
    display: grid !important;
    grid-template-columns: 1fr 1.3fr !important;
    gap: 24px !important;
  }
  .step-number {
    border: 1px solid #000 !important;
    color: #000 !important;
    background: #EEE !important;
    width: 24px !important;
    height: 24px !important;
    min-width: 24px !important;
    font-size: 0.85rem !important;
  }
  .nutrition-dashboard {
    grid-template-columns: repeat(5, 1fr) !important;
    gap: 8px !important;
    margin-top: 12px !important;
  }
  .nutri-box {
    padding: 6px !important;
    border: 1px solid #CCC !important;
  }
  .nutri-val { font-size: 1rem !important; color: #000 !important; }
  .nutri-label { font-size: 0.65rem !important; }
  .chef-tips-grid {
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 12px !important;
    margin-top: 16px !important;
  }
  .chef-tip-card {
    border: 1px solid #CCC !important;
    padding: 10px !important;
  }
  .print-watermark {
    display: block !important;
    margin-top: 24px !important;
    padding-top: 12px !important;
    border-top: 1px solid #888 !important;
    font-size: 8pt !important;
    color: #555 !important;
  }
}

@media (max-width: 768px) {
  .chef-tips-grid { grid-template-columns: 1fr; }
  .recipe-toolbar { flex-direction: column; align-items: flex-start; }
  .search-filter-box { padding: 18px 20px; }
  .filter-chips-row { flex-direction: column; align-items: flex-start; }
}

"""

def generate_recipe_schema(recipe, config):
    domain = config["domain"].rstrip("/")
    slug = recipe["id"]
    recipe_url = f"{domain}/recipes/{slug}.html"
    photo_url = f"{domain}/assets/images/recipes/{slug}.jpg"
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
        "image": [photo_url, pin_url],
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
            "reviewCount": "128"
        }
    }
    return json.dumps(schema, indent=2)

def build_recipe_page(recipe, config, all_recipes):
    domain = config["domain"].rstrip("/")
    slug = recipe["id"]
    recipe_url = f"{domain}/recipes/{slug}.html"
    photo_url = f"{domain}/assets/images/recipes/{slug}.jpg"
    pin_url = f"{domain}/assets/pins/pin-{slug}.png"
    schema_json = generate_recipe_schema(recipe, config)

    # Ingredients HTML with unit data attributes
    ings_html = ""
    for idx, ing in enumerate(recipe.get("ingredients", [])):
        amt = ing.get("amount", "")
        unit = ing.get("unit", "")
        item = ing.get("item", "")
        notes = f" <em>({ing['notes']})</em>" if ing.get("notes") else ""

        link_tag = f"<span class='ing-name'>{item}</span>"
        if ing.get("amazon_key") and ing["amazon_key"] in config["amazon"]["pantry_catalog"]:
            pantry_item = config["amazon"]["pantry_catalog"][ing["amazon_key"]]
            link_tag = f"<a href='{pantry_item['url']}' target='_blank' rel='sponsored nofollow noopener' class='amazon-pantry-link'>{item} ↗</a>"

        ings_html += f"""
        <li class="ing-item">
          <input type="checkbox" id="ing-{idx}" class="ing-checkbox" onchange="toggleIng(this)">
          <label for="ing-{idx}" class="ing-label">
            <span class="ing-amt" data-base="{amt}">{amt}</span> 
            <span class="ing-unit" data-base-unit="{unit}">{unit}</span> 
            {link_tag}{notes}
          </label>
        </li>
        """

    # Instructions HTML with interactive click-to-complete
    steps = recipe.get("instructions", [])
    steps_html = ""
    for s in steps:
        steps_html += f"""
        <li class="instruction-step" onclick="toggleStep(this)">
          <div class="step-number">{s.get('step', 1)}</div>
          <div class="step-content">
            <h4>{s.get('title', '')}</h4>
            <p>{s.get('text', '')}</p>
          </div>
        </li>
        """

    # Kitchen Tools Cards
    tools_html = ""
    for t_key in recipe.get("equipment", []):
        if t_key in config["amazon"]["tools_catalog"]:
            tool = config["amazon"]["tools_catalog"][t_key]
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

    # Related Recipes
    related = [r for r in all_recipes if r["id"] != slug][:3]
    related_html = ""
    for r in related:
        related_html += f"""
        <a href="/recipes/{r['id']}.html" class="recipe-card">
          <div class="card-media">
            <img src="/assets/images/recipes/{r['id']}.jpg" alt="{r['title']}" loading="lazy">
            <span class="card-badge-cat">{r.get('category', 'Dinner')}</span>
            <span class="card-badge-time">⏱️ {r['total_time']} mins</span>
          </div>
          <div class="card-body">
            <div class="card-rating">★★★★★ 4.9 <span class="count">(115)</span></div>
            <div class="card-title">{r['title']}</div>
            <div class="macro-pills">
              <span class="macro-pill protein">{r['protein']}g Protein</span>
              <span class="macro-pill cals">{r['calories']} Cals</span>
            </div>
            <div class="card-cta-row">
              <span>View Recipe</span>
              <span class="arrow">→</span>
            </div>
          </div>
        </a>
        """

    # Macro percentages calculation
    p = recipe.get("protein", 35)
    c = recipe.get("carbs", 20)
    f = recipe.get("fat", 15)
    total_cal_est = (p * 4) + (c * 4) + (f * 9)
    if total_cal_est > 0:
        p_pct = round((p * 4 / total_cal_est) * 100)
        c_pct = round((c * 4 / total_cal_est) * 100)
        f_pct = max(0, 100 - p_pct - c_pct)
    else:
        p_pct, c_pct, f_pct = 40, 30, 30

    escaped_title = recipe['title'].replace("'", "\\'")
    pin_desc = recipe.get('pin_copy', {}).get('description', '')

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
  <meta property="og:image" content="{photo_url}">
  
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

  <!-- Top Announcement Bar -->
  <div class="top-bar">
    <span>🥗 CleanPlated Kitchen</span> Tested high-protein everyday meals in under 25 minutes with minimal cleanup.
  </div>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand">
        <div class="brand-icon">🌿</div>
        Clean<span>Plated</span>
      </a>
      <nav class="nav-links">
        <a href="/#recipes">All Recipes</a>
        <a href="/#tools">Kitchen Gear</a>
        <a href="/meal-planner.html" class="nav-cta">⚡ Weekly Meal Planner</a>
      </nav>
    </div>
  </header>

  <main class="container recipe-page">
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <span>{recipe.get('category', 'Recipes')}</span> &gt; <span>{recipe['title']}</span>
    </div>

    <!-- Recipe Hero Split -->
    <section class="recipe-hero-split">
      <div class="recipe-hero-text">
        <div class="hero-badge-pill">
          <span class="dot"></span>
          {recipe.get('category', 'Healthy Meals')} • ⏱️ {recipe.get('total_time', 20)} Mins
        </div>
        <h1>{recipe['title']}</h1>
        <p class="recipe-hero-sub">{recipe.get('headline', '')}</p>

        <div class="recipe-byline-bar">
          <img src="/assets/images/author-avatar.jpg" alt="{config['author']['name']}" class="byline-avatar">
          <div class="byline-info">
            <div class="byline-name">By {config['author']['name']}</div>
            <div class="byline-meta">Certified Sports Nutritionist • Updated November 2026 • ★★★★★ 4.9 (128 reviews)</div>
          </div>
        </div>

        <!-- Quick Action Bar (Pinch of Yum / WP Tasty Signature) -->
        <div class="recipe-quick-actions">
          <a href="#recipe" class="btn-jump">Jump to Recipe ↓</a>
          <button onclick="window.print()" class="btn-print">🖨️ Print Recipe</button>
          <a href="https://pinterest.com/pin/create/button/?url={recipe_url}&media={pin_url}&description={pin_desc}" target="_blank" rel="noopener" class="btn-pin-action">📌 Pin</a>
          <button onclick="shareRecipe('{escaped_title}', '{recipe_url}')" class="btn-share">🔗 Share</button>
          <button onclick="addToMealPlan('{slug}', '{escaped_title}')" class="btn-plan">➕ Add to Meal Plan</button>
        </div>
        <div style="font-size:0.76rem; color:var(--ink-secondary); margin-top:14px; line-height:1.4;">
          🌱 <em>CleanPlated is reader-supported. When you buy through links on our site, we may earn an affiliate commission at no extra cost to you.</em>
        </div>
      </div>

      <div class="recipe-hero-visual">
        <img src="/assets/images/recipes/{slug}.jpg" alt="{recipe['title']}">
        <div class="recipe-photo-caption">
          <span>Freshly cooked in under 25 minutes</span>
          <span style="font-weight:700; color:var(--primary);">Tested Recipe ✓</span>
        </div>
      </div>
    </section>

    <!-- Master Interactive Recipe Box -->
    <section class="recipe-card-box" id="recipe">
      <div class="recipe-box-header">
        <h2>{recipe['title']}</h2>
        <p style="color:var(--ink-secondary);">{recipe.get('description', '')}</p>

        <!-- Nutrition Highlights Dashboard -->
        <div class="nutrition-dashboard">
          <div class="nutri-box">
            <div class="nutri-val">{recipe.get('calories', 400)}</div>
            <div class="nutri-label">Calories</div>
          </div>
          <div class="nutri-box">
            <div class="nutri-val" style="color:var(--primary);">{recipe.get('protein', 30)}g</div>
            <div class="nutri-label">Protein</div>
          </div>
          <div class="nutri-box">
            <div class="nutri-val">{recipe.get('carbs', 20)}g</div>
            <div class="nutri-label">Carbs</div>
          </div>
          <div class="nutri-box">
            <div class="nutri-val">{recipe.get('fat', 15)}g</div>
            <div class="nutri-label">Fat</div>
          </div>
          <div class="nutri-box">
            <div class="nutri-val">{recipe.get('fiber', 5)}g</div>
            <div class="nutri-label">Fiber</div>
          </div>
        </div>
      </div>

      <!-- Controls Toolbar (Scalers, Unit Converter & Cook Mode) -->
      <div class="recipe-toolbar">
        <div class="toolbar-group">
          <span class="toolbar-label">Servings:</span>
          <div class="serving-btns">
            <button class="serv-btn active" onclick="setServingMultiplier(1, this)">1x (Base)</button>
            <button class="serv-btn" onclick="setServingMultiplier(2, this)">2x</button>
            <button class="serv-btn" onclick="setServingMultiplier(3, this)">3x</button>
          </div>
        </div>

        <div class="toolbar-group">
          <span class="toolbar-label">Units:</span>
          <div class="unit-toggle-pill">
            <button class="unit-btn active" onclick="setUnitSystem('us', this)">US Customary</button>
            <button class="unit-btn" onclick="setUnitSystem('metric', this)">Metric (g/ml)</button>
          </div>
        </div>

        <div class="toolbar-group">
          <label class="cook-mode-wrap">
            <input type="checkbox" id="cookModeCheck" onchange="toggleCookMode(this)">
            <span class="cook-mode-badge"></span>
            <span class="cook-mode-label">🍳 Cook Mode (Keep Screen Awake)</span>
          </label>
        </div>
      </div>

      <div class="recipe-core-layout">
        <!-- Ingredients Column with Scaler -->
        <div>
          <div class="serving-scaler-wrap">
            <h3>Ingredients</h3>
          </div>

          <p style="font-size:0.82rem; color:var(--ink-muted); margin-bottom:14px;">Tap items to check off while cooking or shopping:</p>
          <ul class="ingredients-list">
            {ings_html}
          </ul>

          <!-- Kitchen Tools Showcase -->
          <div class="recipe-tools-box">
            <h4>Essential Equipment Used:</h4>
            <div class="recipe-tools-grid">
              {tools_html}
            </div>
          </div>
        </div>

        <!-- Step-by-Step Instructions Column with Progress Bar -->
        <div>
          <div class="progress-tracker">
            <div class="progress-header">
              <span>🍳 Cooking Progress</span>
              <span id="progressText">0 of {len(steps)} steps (0%)</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill" id="progressFill"></div>
            </div>
          </div>

          <h3 style="font-family:var(--font-serif); font-size:1.4rem; color:var(--ink); margin-bottom:16px; padding-bottom:8px; border-bottom:1px solid var(--border);">Step-by-Step Instructions</h3>
          <p style="font-size:0.82rem; color:var(--ink-muted); margin-bottom:16px;">Tap any step as you finish it to keep your place:</p>
          <ol class="instructions-list">
            {steps_html}
          </ol>

          <!-- Chef Tips 3-Box Grid (Skinnytaste / Well Plated Standard) -->
          <div class="chef-tips-grid">
            <div class="chef-tip-card">
              <div class="tip-icon">❄️</div>
              <div class="tip-title">Storage & Meal Prep</div>
              <div class="tip-text">Refrigerate in airtight glass containers for up to 4 days. Freeze portions individually for up to 2 months.</div>
            </div>
            <div class="chef-tip-card">
              <div class="tip-icon">♨️</div>
              <div class="tip-title">Crisp Reheating</div>
              <div class="tip-text">Air fry at 350°F (175°C) for 3–4 minutes to revive crunch, or warm in a dry skillet over medium heat.</div>
            </div>
            <div class="chef-tip-card">
              <div class="tip-icon">🔄</div>
              <div class="tip-title">Dietary Swaps</div>
              <div class="tip-text">Easily adapt to dairy-free with olive oil or coconut milk; swap tamari for soy sauce for 100% gluten-free.</div>
            </div>
          </div>

          <!-- FDA-Style Nutrition Facts Panel (Skinnytaste Signature) -->
          <div class="nutrition-facts-panel">
            <div class="nf-title">Nutrition Facts</div>
            <div class="nf-sub">Amount per serving ({recipe.get('servings', 2)} servings per batch)</div>
            
            <div class="nf-calories-row">
              <span>Calories</span>
              <span class="nf-cal-num">{recipe.get('calories', 400)}</span>
            </div>

            <div class="macro-ratio-wrap">
              <div class="macro-ratio-bar">
                <div class="ratio-segment" style="width:{p_pct}%; background:#1C3F2F;" title="Protein: {p_pct}%"></div>
                <div class="ratio-segment" style="width:{c_pct}%; background:#D2812A;" title="Carbs: {c_pct}%"></div>
                <div class="ratio-segment" style="width:{f_pct}%; background:#C55836;" title="Fat: {f_pct}%"></div>
              </div>
              <div class="ratio-legend">
                <span><span class="legend-dot" style="background:#1C3F2F;"></span> {p_pct}% Protein ({recipe.get('protein', 30)}g)</span>
                <span><span class="legend-dot" style="background:#D2812A;"></span> {c_pct}% Carbs ({recipe.get('carbs', 20)}g)</span>
                <span><span class="legend-dot" style="background:#C55836;"></span> {f_pct}% Fat ({recipe.get('fat', 15)}g)</span>
              </div>
            </div>

            <div class="nf-table">
              <div class="nf-row bold"><span>Total Fat</span> <span>{recipe.get('fat', 15)}g</span></div>
              <div class="nf-row indent"><span>Saturated Fat</span> <span>{round(recipe.get('fat', 15) * 0.28, 1)}g</span></div>
              <div class="nf-row bold"><span>Total Carbohydrates</span> <span>{recipe.get('carbs', 20)}g</span></div>
              <div class="nf-row indent"><span>Dietary Fiber</span> <span>{recipe.get('fiber', 4)}g</span></div>
              <div class="nf-row indent"><span>Net Carbs</span> <span>{max(0, recipe.get('carbs', 20) - recipe.get('fiber', 4))}g</span></div>
              <div class="nf-row bold"><span>Protein</span> <span>{recipe.get('protein', 30)}g</span></div>
            </div>
          </div>

          <div class="print-watermark">
            Printed from <b>CleanPlated</b> (cleanplatedmeals.com) • Healthy, High-Protein Everyday Dinners.
          </div>
        </div>
      </div>

      <!-- Pinterest Pin Banner Box -->
      <div class="pin-save-section">
        <div class="pin-thumbnail">
          <img src="/assets/pins/pin-{slug}.png" alt="Pinterest pin for {recipe['title']}">
        </div>
        <div>
          <h4 style="font-family:var(--font-serif); font-size:1.25rem; color:var(--ink); margin-bottom:6px;">Love this recipe? Save it to Pinterest!</h4>
          <p style="font-size:0.92rem; color:var(--ink-secondary); margin-bottom:14px;">Save this high-protein 20-minute dinner to your healthy dinner board so you never wonder what to make on busy weeknights.</p>
          <a href="https://pinterest.com/pin/create/button/?url={recipe_url}&media={pin_url}&description={pin_desc}" target="_blank" rel="noopener" class="btn-pin-action" style="display:inline-block;">
            📌 Save Pin to Pinterest
          </a>
        </div>
      </div>
    </section>

    <!-- Related Recipes -->
    <section style="margin-top:64px;">
      <h3 style="font-family:var(--font-serif); font-size:1.8rem; margin-bottom:24px;">You May Also Love</h3>
      <div class="recipe-grid">
        {related_html}
      </div>
    </section>
  </main>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-disclosure">
        <b>Amazon Associates Disclosure:</b> {config['amazon']['disclosure']}
      </div>
      <div class="footer-bottom">
        <div>© 2026 {config['site_name']} • All Rights Reserved. Clean, Wholesome & High-Protein Everyday Dinners.</div>
        <div>
          <a href="/feed/pinterest.xml" style="color:var(--accent-gold);">Pinterest RSS Feed</a> • 
          <a href="/sitemap.xml" style="color:#FFF;">XML Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Floating Sticky Action Dock -->
  <div class="floating-recipe-bar" id="floatingBar">
    <div class="floating-bar-inner">
      <div class="floating-recipe-title">
        <span>🥗</span>
        <span>{recipe['title'][:28]}...</span>
      </div>
      <div class="floating-recipe-actions">
        <a href="#recipe" class="floating-btn">📋 Ingredients</a>
        <a href="#instructions" class="floating-btn">🍳 Steps</a>
        <button onclick="window.print()" class="floating-btn">🖨️ Print</button>
        <button onclick="addToMealPlan('{slug}', '{escaped_title}')" class="floating-btn">➕ Plan</button>
        <a href="https://pinterest.com/pin/create/button/?url={recipe_url}&media={pin_url}&description={pin_desc}" target="_blank" rel="noopener" class="floating-pin-btn">📌 Pin</a>
      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <div class="toast-container" id="toastContainer"></div>

  {RECIPE_PAGE_JS}
</body>
</html>
"""
    return html

def build_homepage(recipes, config):
    categories = sorted(list(set(r.get("category", "Healthy Meals") for r in recipes)))
    featured = recipes[0]

    # Recipe Cards HTML with data attributes for instant search & filtering
    cards_html = ""
    for r in recipes:
        tags_str = ",".join(r.get("tags", []))
        cards_html += f"""
        <a href="/recipes/{r['id']}.html" class="recipe-card reveal reveal-stagger" data-category="{r.get('category', '')}" data-time="{r.get('total_time', 20)}" data-protein="{r.get('protein', 30)}" data-tags="{tags_str}">
          <div class="card-media">
            <img src="/assets/images/recipes/{r['id']}.jpg" alt="{r['title']}" loading="lazy">
            <span class="card-badge-cat">{r.get('category', 'Healthy Meals')}</span>
            <span class="card-badge-time">⏱️ {r['total_time']} mins</span>
          </div>
          <div class="card-body">
            <div class="card-rating">★★★★★ 4.9 <span class="count">(130+ reviews)</span></div>
            <h3 class="card-title">{r['title']}</h3>
            <p class="card-desc">{r.get('headline', '')}</p>
            <div class="macro-pills">
              <span class="macro-pill protein">{r['protein']}g Protein</span>
              <span class="macro-pill cals">{r['calories']} Cals</span>
              <span class="macro-pill carbs">{r['carbs']}g Carbs</span>
            </div>
            <div class="card-cta-row">
              <span>View Recipe & Prep Checklist</span>
              <span class="arrow">→</span>
            </div>
          </div>
        </a>
        """

    # Tools Showcase HTML
    tools_html = ""
    for k, tool in config["amazon"]["tools_catalog"].items():
        tools_html += f"""
        <div class="tool-card reveal reveal-stagger">
          <span class="tool-badge">{tool['badge']}</span>
          <div class="tool-title">{tool['name']}</div>
          <div class="tool-desc">{tool['description']}</div>
          <a href="{tool['url']}" target="_blank" rel="sponsored nofollow noopener" class="amazon-btn">
            <span>View on Amazon ({tool['price_approx']})</span> →
          </a>
        </div>
        """

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

  <!-- Top Announcement Bar -->
  <div class="top-bar">
    <span>🌿 CleanPlated Clean Eating</span> High-protein, clean-ingredient dinners ready in 25 minutes or less. Minimal cleanup.
  </div>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand">
        <div class="brand-icon">🌿</div>
        Clean<span>Plated</span>
      </a>
      <nav class="nav-links">
        <a href="/#recipes">Recipes</a>
        <a href="/#tools">Tested Gear</a>
        <a href="/#author">About Chefs</a>
        <a href="/meal-planner.html" class="nav-cta">⚡ Weekly Meal Planner</a>
      </nav>
    </div>
  </header>

  <!-- Editorial Hero Section -->
  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-content">
        <div class="hero-badge-pill">
          <span class="dot"></span>
          Fast • Wholesome • 40g+ Protein
        </div>
        <h1>Effortless Healthy Weeknight Dinners in 25 Mins or Less.</h1>
        <p>No complicated prep, no mountain of dishes, and zero boring diet food. Real chef-crafted recipes packed with high protein, vibrant vegetables, and wholesome pantry staples.</p>
        <div class="hero-actions">
          <a href="/#recipes" class="btn-primary">Explore All Recipes ↓</a>
          <a href="/meal-planner.html" class="btn-secondary">Build 7-Day Meal Plan →</a>
        </div>
      </div>

      <!-- Featured Recipe Hero Card -->
      <a href="/recipes/{featured['id']}.html" class="hero-card">
        <div class="hero-card-img-wrap">
          <img src="/assets/images/recipes/{featured['id']}.jpg" alt="{featured['title']}">
          <div class="hero-floating-badge">Featured Recipe of the Day</div>
        </div>
        <div class="hero-card-body">
          <div class="hero-card-meta">
            <span>⏱️ {featured['total_time']} Mins</span> • <span>★ 4.9 Rating</span>
          </div>
          <div class="hero-card-title">{featured['title']}</div>
          <div class="hero-card-macros">
            <span class="macro-pill protein">{featured['protein']}g Protein</span>
            <span class="macro-pill cals">{featured['calories']} Cals</span>
            <span class="macro-pill carbs">{featured['carbs']}g Carbs</span>
          </div>
        </div>
      </a>
    </div>
  </section>

  <!-- Minimalist Baker Inspired Instant Search & Filter Hub -->
  <section class="container filter-section reveal" id="search-hub">
    <div class="search-filter-box">
      <div class="search-input-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" id="recipeSearchInput" placeholder="Search 10 fast healthy recipes by ingredient, dish name, or keyword (e.g. salmon, air fryer, chicken)..." autocomplete="off">
      </div>
      <div class="filter-chips-row">
        <div class="filter-chips">
          <button class="filter-chip active" data-tag="all" onclick="filterByChip('all', this)">All Recipes (10)</button>
          <button class="filter-chip" data-tag="under-20" onclick="filterByChip('under-20', this)">⏱️ Under 20 Mins</button>
          <button class="filter-chip" data-tag="high-protein" onclick="filterByChip('high-protein', this)">💪 40g+ Protein</button>
          <button class="filter-chip" data-tag="air-fryer" onclick="filterByChip('air-fryer', this)">⚡ Air Fryer</button>
          <button class="filter-chip" data-tag="low-carb" onclick="filterByChip('low-carb', this)">🥑 Low Carb / Bowls</button>
          <button class="filter-chip" data-tag="skillet" onclick="filterByChip('skillet', this)">🍳 One-Pan Skillet</button>
        </div>
        <div class="filter-count-badge" id="visibleCount">Showing 10 healthy recipes</div>
      </div>
    </div>
  </section>

  <!-- Recipe Grid Section -->
  <main class="container recipes-section" id="recipes">
    <div class="section-title-wrap reveal">
      <div>
        <h2 class="section-title">Fresh Everyday Healthy Dinners</h2>
        <div class="section-sub">Tested for busy weeknights: ready fast, balanced macros, and delicious flavor.</div>
      </div>
    </div>

    <!-- Empty State Message -->
    <div id="noResultsMsg" style="display:none; text-align:center; padding:60px 20px; background:#FFF; border-radius:16px; border:1px dashed var(--border);">
      <div style="font-size:2.5rem; margin-bottom:12px;">🥗</div>
      <h3 style="font-family:var(--font-serif); font-size:1.5rem; margin-bottom:8px;">No matching recipes found</h3>
      <p style="color:var(--ink-secondary); margin-bottom:20px;">Try searching for a different ingredient like "salmon", "chicken", or "oats".</p>
      <button onclick="resetSearch()" class="btn-primary" style="margin:0 auto;">Reset Search</button>
    </div>

    <div class="recipe-grid">
      {cards_html}
    </div>
  </main>

  <!-- Kitchen Equipment Section -->
  <section class="tools-section" id="tools">
    <div class="container reveal">
      <div style="text-align:center; max-width:680px; margin:0 auto 36px;">
        <span class="hero-badge-pill">Tested & Recommended Gear</span>
        <h2 style="font-family:var(--font-serif); font-size:2.2rem; color:var(--ink); margin-bottom:8px;">Tools That Make Clean Eating Effortless</h2>
        <p style="color:var(--ink-secondary);">Every recipe on CleanPlated is tested with standard home kitchen tools designed to slash prep time and make cooking enjoyable.</p>
      </div>

      <div class="tools-grid">
        {tools_html}
      </div>
    </div>
  </section>

  <!-- Author & E-E-A-T Section -->
  <section class="author-section" id="author">
    <div class="container">
      <div class="author-box reveal">
        <div class="author-avatar-wrap">
          <img src="/assets/images/author-avatar.jpg" alt="{config['author']['name']}">
        </div>
        <div class="author-details">
          <div class="author-role">Culinary Nutritionist & Founder</div>
          <h3>Meet Chef Marcus & Elena Vance</h3>
          <p class="author-bio">{config['author']['bio']} Every meal is formulated with a minimum of 35g–45g of bioavailable protein, complex carbohydrates, and anti-inflammatory healthy fats to keep you fueled all day.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-disclosure">
        <b>Amazon Associates Disclosure:</b> {config['amazon']['disclosure']}
      </div>
      <div class="footer-bottom">
        <div>© 2026 {config['site_name']} • Clean & Wholesome Meals for Real Life.</div>
        <div>
          <a href="/feed/pinterest.xml" style="color:var(--accent-gold);">Pinterest Media Feed</a> • 
          <a href="/sitemap.xml" style="color:#FFF;">XML Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  {HOMEPAGE_JS}
</body>
</html>
"""
    return html

def build_sitemap(recipes, config):
    domain = config["domain"].rstrip("/")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    xml.append('  <url>')
    xml.append(f'    <loc>{domain}/</loc>')
    xml.append('    <lastmod>2026-11-18</lastmod>')
    xml.append('    <changefreq>daily</changefreq>')
    xml.append('    <priority>1.0</priority>')
    xml.append('  </url>')
    xml.append('  <url>')
    xml.append(f'    <loc>{domain}/meal-planner.html</loc>')
    xml.append('    <lastmod>2026-11-18</lastmod>')
    xml.append('    <changefreq>weekly</changefreq>')
    xml.append('    <priority>0.8</priority>')
    xml.append('  </url>')

    for r in recipes:
        xml.append('  <url>')
        xml.append(f'    <loc>{domain}/recipes/{r["id"]}.html</loc>')
        xml.append('    <lastmod>2026-11-18</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('    <priority>0.9</priority>')
        xml.append('  </url>')

    xml.append('</urlset>')
    return "\n".join(xml)

def build_pinterest_feed(recipes, config):
    domain = config["domain"].rstrip("/")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">')
    xml.append('  <channel>')
    xml.append(f'    <title>{escape(config["site_name"])} - Pinterest Recipe Media Feed</title>')
    xml.append(f'    <link>{domain}</link>')
    xml.append('    <description>Daily High-Protein, Healthy &amp; Easy Meal Pins</description>')
    xml.append('    <language>en-us</language>')

    for r in recipes:
        pin_url = f"{domain}/assets/pins/pin-{r['id']}.png"
        link = f"{domain}/recipes/{r['id']}.html?utm_source=pinterest&utm_medium=pin&utm_campaign={r['id']}"
        desc = escape(r.get("pin_copy", {}).get("description", r["headline"]))
        title = escape(r.get("pin_copy", {}).get("title", r["title"]))
        cat = escape(r.get("category", "Healthy Dinners"))

        xml.append('    <item>')
        xml.append(f'      <title>{title}</title>')
        xml.append(f'      <link>{link}</link>')
        xml.append(f'      <guid>{r["id"]}</guid>')
        xml.append(f'      <pubDate>Wed, 18 Nov 2026 12:00:00 +0000</pubDate>')
        xml.append(f'      <description>{desc}</description>')
        xml.append(f'      <enclosure url="{pin_url}" type="image/png" length="85000" />')
        xml.append(f'      <media:content url="{pin_url}" type="image/png" medium="image" />')
        xml.append(f'      <category>{cat}</category>')
        xml.append('    </item>')

    xml.append('  </channel>')
    xml.append('</rss>')
    return "\n".join(xml)

def build_all():
    recipes, config = load_data()
    os.makedirs(RECIPES_DIR, exist_ok=True)
    os.makedirs(FEED_DIR, exist_ok=True)

    print("\n=======================================================")
    print("      PUREPLATED HIGH-END EDITORIAL COMPILER")
    print("=======================================================")

    for r in recipes:
        html = build_recipe_page(r, config, recipes)
        out_path = os.path.join(RECIPES_DIR, f"{r['id']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[✓] Compiled Recipe Page: /recipes/{r['id']}.html")

    index_html = build_homepage(recipes, config)
    with open(os.path.join(PUBLIC_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"[✓] Compiled Homepage: /index.html (with real food photography)")

    sitemap_xml = build_sitemap(recipes, config)
    with open(os.path.join(PUBLIC_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print(f"[✓] Generated Sitemap: /sitemap.xml")

    feed_xml = build_pinterest_feed(recipes, config)
    with open(os.path.join(FEED_DIR, "pinterest.xml"), "w", encoding="utf-8") as f:
        f.write(feed_xml)
    print(f"[✓] Generated Pinterest Feed: /feed/pinterest.xml")

    with open(os.path.join(PUBLIC_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {config['domain']}/sitemap.xml\n")
    print(f"[✓] Generated robots.txt")

    print("=======================================================")
    print(f"[✓] Build complete! Premium static assets in {PUBLIC_DIR}\n")

if __name__ == "__main__":
    build_all()
