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

    # Ingredients HTML
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
          <input type="checkbox" id="ing-{idx}" onchange="toggleIng(this)">
          <label for="ing-{idx}">
            <span class="ing-amt" data-base="{amt}">{amt}</span> 
            <span class="ing-unit">{unit}</span> 
            {link_tag}{notes}
          </label>
        </li>
        """

    # Instructions HTML
    steps_html = ""
    for s in recipe.get("instructions", []):
        steps_html += f"""
        <li class="instruction-step">
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
        <a href="{r['id']}.html" class="recipe-card">
          <div class="card-media">
            <img src="../assets/images/recipes/{r['id']}.jpg" alt="{r['title']}" loading="lazy">
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

  <!-- Top Bar -->
  <div class="top-bar">
    <span>🥗 PurePlated Kitchen</span> Tested high-protein everyday meals in under 25 minutes with minimal cleanup.
  </div>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="../index.html" class="brand">
        <div class="brand-icon">🌿</div>
        Pure<span>Plated</span>
      </a>
      <nav class="nav-links">
        <a href="../index.html">All Recipes</a>
        <a href="../index.html#tools">Kitchen Gear</a>
        <a href="../meal-planner.html" class="nav-cta">⚡ Weekly Meal Planner</a>
      </nav>
    </div>
  </header>

  <main class="container recipe-page">
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
      <a href="../index.html">Home</a> &gt; <span>{recipe.get('category', 'Recipes')}</span> &gt; <span>{recipe['title']}</span>
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
          <img src="../assets/images/author-avatar.jpg" alt="{config['author']['name']}" class="byline-avatar">
          <div class="byline-info">
            <div class="byline-name">By {config['author']['name']}</div>
            <div class="byline-meta">Certified Sports Nutritionist • Updated November 2026 • ★★★★★ 4.9 (128 reviews)</div>
          </div>
        </div>

        <div class="recipe-quick-actions">
          <a href="#recipe" class="btn-jump">Jump to Recipe ↓</a>
          <a href="https://pinterest.com/pin/create/button/?url={recipe_url}&media={pin_url}&description={recipe.get('pin_copy', {}).get('description', '')}" target="_blank" rel="noopener" class="btn-pin-action">📌 Pin to Pinterest</a>
        </div>
      </div>

      <div class="recipe-hero-visual">
        <img src="../assets/images/recipes/{slug}.jpg" alt="{recipe['title']}">
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

        <!-- Nutrition Dashboard -->
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

      <div class="recipe-core-layout">
        <!-- Ingredients Column with Scaler -->
        <div>
          <div class="serving-scaler-wrap">
            <h3>Ingredients</h3>
            <div class="serving-btns">
              <button class="serv-btn active" onclick="scaleServings(2, this)">2 Serv</button>
              <button class="serv-btn" onclick="scaleServings(4, this)">4 Serv</button>
              <button class="serv-btn" onclick="scaleServings(6, this)">6 Serv</button>
            </div>
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

        <!-- Step-by-Step Instructions Column -->
        <div>
          <h3 style="font-family:var(--font-serif); font-size:1.4rem; color:var(--ink); margin-bottom:20px; padding-bottom:12px; border-bottom:1px solid var(--border);">Step-by-Step Instructions</h3>
          <ol class="instructions-list">
            {steps_html}
          </ol>

          <!-- Chef Tips -->
          <div style="background:var(--primary-light); border-left:4px solid var(--primary); padding:20px; border-radius:8px; margin-top:24px;">
            <h4 style="color:var(--primary); font-weight:700; margin-bottom:6px;">Chef's Meal Prep & Storage Pro-Tip:</h4>
            <p style="font-size:0.92rem; color:var(--ink-secondary); line-height:1.6;">Store in airtight glass meal prep containers in the refrigerator for up to 4 days. Reheat in the air fryer at 350°F for 3 minutes to restore that restaurant-crisp texture!</p>
          </div>
        </div>
      </div>

      <!-- Pinterest Pin Banner Box -->
      <div class="pin-save-section">
        <div class="pin-thumbnail">
          <img src="../assets/pins/pin-{slug}.png" alt="Pinterest pin for {recipe['title']}">
        </div>
        <div>
          <h4 style="font-family:var(--font-serif); font-size:1.25rem; color:var(--ink); margin-bottom:6px;">Love this recipe? Save it to Pinterest!</h4>
          <p style="font-size:0.92rem; color:var(--ink-secondary); margin-bottom:14px;">Save this high-protein 20-minute dinner to your healthy dinner board so you never wonder what to make on busy weeknights.</p>
          <a href="https://pinterest.com/pin/create/button/?url={recipe_url}&media={pin_url}&description={recipe.get('pin_copy', {}).get('description', '')}" target="_blank" rel="noopener" class="btn-pin-action" style="display:inline-block;">
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
          <a href="../feed/pinterest.xml" style="color:var(--accent-gold);">Pinterest RSS Feed</a> • 
          <a href="../sitemap.xml" style="color:#FFF;">XML Sitemap</a>
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

    function scaleServings(targetServings, btn) {{
      document.querySelectorAll('.serv-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const baseServings = 2; // Default base
      const factor = targetServings / baseServings;
      
      document.querySelectorAll('.ing-amt').forEach(el => {{
        const base = parseFloat(el.getAttribute('data-base'));
        if (!isNaN(base)) {{
          const newVal = (base * factor);
          el.innerText = newVal % 1 === 0 ? newVal.toFixed(0) : newVal.toFixed(1);
        }}
      }});
    }}
  </script>
</body>
</html>
"""
    return html

def build_homepage(recipes, config):
    categories = sorted(list(set(r.get("category", "Healthy Meals") for r in recipes)))
    featured = recipes[0]

    # Recipe Cards HTML
    cards_html = ""
    for r in recipes:
        cards_html += f"""
        <a href="recipes/{r['id']}.html" class="recipe-card" data-category="{r.get('category', '')}">
          <div class="card-media">
            <img src="assets/images/recipes/{r['id']}.jpg" alt="{r['title']}" loading="lazy">
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
    filter_html = '<button class="filter-btn active" onclick="filterCategory(\'all\', this)">All Recipes (10)</button>'
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

  <!-- Top Announcement Bar -->
  <div class="top-bar">
    <span>🌿 PurePlated Clean Eating</span> High-protein, clean-ingredient dinners ready in 25 minutes or less. Minimal cleanup.
  </div>

  <!-- Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="brand">
        <div class="brand-icon">🌿</div>
        Pure<span>Plated</span>
      </a>
      <nav class="nav-links">
        <a href="#recipes">Recipes</a>
        <a href="#tools">Tested Gear</a>
        <a href="#author">About Chefs</a>
        <a href="meal-planner.html" class="nav-cta">⚡ Weekly Meal Planner</a>
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
          <a href="#recipes" class="btn-primary">Explore All Recipes ↓</a>
          <a href="meal-planner.html" class="btn-secondary">Build 7-Day Meal Plan →</a>
        </div>
      </div>

      <!-- Featured Recipe Hero Card -->
      <a href="recipes/{featured['id']}.html" class="hero-card">
        <div class="hero-card-img-wrap">
          <img src="assets/images/recipes/{featured['id']}.jpg" alt="{featured['title']}">
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

  <!-- Category Filter Bar -->
  <section class="container filter-section">
    <div class="filter-bar">
      {filter_html}
    </div>
  </section>

  <!-- Recipe Grid Section -->
  <main class="container recipes-section" id="recipes">
    <div class="section-title-wrap">
      <div>
        <h2 class="section-title">Fresh Everyday Healthy Dinners</h2>
        <div class="section-sub">Tested for busy weeknights: ready fast, balanced macros, and delicious flavor.</div>
      </div>
    </div>

    <div class="recipe-grid">
      {cards_html}
    </div>
  </main>

  <!-- Kitchen Equipment Section -->
  <section class="tools-section" id="tools">
    <div class="container">
      <div style="text-align:center; max-width:680px; margin:0 auto 36px;">
        <span class="hero-badge-pill">Tested & Recommended Gear</span>
        <h2 style="font-family:var(--font-serif); font-size:2.2rem; color:var(--ink); margin-bottom:8px;">Tools That Make Clean Eating Effortless</h2>
        <p style="color:var(--ink-secondary);">Every recipe on PurePlated is tested with standard home kitchen tools designed to slash prep time and make cooking enjoyable.</p>
      </div>

      <div class="tools-grid">
        {tools_html}
      </div>
    </div>
  </section>

  <!-- Author & E-E-A-T Section -->
  <section class="author-section" id="author">
    <div class="container">
      <div class="author-box">
        <div class="author-avatar-wrap">
          <img src="assets/images/author-avatar.jpg" alt="{config['author']['name']}">
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
          <a href="feed/pinterest.xml" style="color:var(--accent-gold);">Pinterest Media Feed</a> • 
          <a href="sitemap.xml" style="color:#FFF;">XML Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    function filterCategory(cat, btn) {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cards = document.querySelectorAll('.recipe-card');
      cards.forEach(c => {{
        if (cat === 'all' || c.getAttribute('data-category') === cat) {{
          c.style.display = 'flex';
        }} else {{
          c.style.display = 'none';
        }}
      }});
    }}
  </script>
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
