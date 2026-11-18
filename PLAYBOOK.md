# PurePlated Operations & Traffic Scaling Playbook

This playbook walks you through running, monetizing, and scaling **PurePlated** to $3,000–$10,000/month with Amazon Affiliate commissions and Pinterest viral traffic.

---

## 1. Quick Start Setup (5 Minutes)

### Step 1: Set Your Amazon Associates Tag
Open `config/site_config.json`:
```json
"amazon": {
  "affiliate_tag": "yourtag-20"
}
```
Replace `cleanplated-20` with your active Amazon Associates Tracking ID. All product buttons, kitchen tool showcases, and inline pantry links will immediately inherit your tag on the next build!

### Step 2: Deploy to Web Hosting
The `public/` directory contains 100% static HTML, CSS, JS, and image assets with zero database overhead. You can host it virtually anywhere for free or near-zero cost:

* **Option A: Hostinger (Your existing server)**
  Upload the contents of `/home/hamzazahid8/daily-healthy-meals/public/` to your `public_html` directory (or a subdomain like `meals.aipilotmoney.com` or `pureplated.com`).
* **Option B: Cloudflare Pages / Vercel / Netlify**
  Connect your GitHub repository and set the publish directory to `public`. Cloudflare Pages provides unlimited free bandwidth, global CDN caching, and automated HTTPS.
* **Option C: Local Testing**
  ```bash
  python3 -m http.server 8080 --directory public/
  ```

---

## 2. Pinterest Traffic & Board Strategy

Pinterest is an image search engine with over 450M hungry users actively searching for recipe inspiration.

### A. Recommended Boards to Create on Pinterest
Set up 5 core public boards on your Pinterest Business account:
1. **Quick & Healthy Easy Meals (Primary)**
2. **High-Protein Dinners (< 25 Mins)**
3. **Clean Eating Meal Prep Ideas**
4. **Air Fryer Healthy Recipes**
5. **Low-Carb & Keto Weeknight Dinners**

### B. Pin Publishing Frequency
* **Frequency:** 2 pins per day (Optimal times: 8:00 AM EST and 5:00 PM EST).
* **Why this works:** Consistent daily pinning signals to Pinterest's Smart Feed algorithm that your account is an active authority, unlocking algorithmic recommendation traffic in related home feeds.

### C. Activating the Make.com Scenario
Your Make.com scenario is already created under Scenario ID **`7094447`**!
1. Visit [Make.com Scenario 7094447](https://us2.make.com/2010020/scenarios/7094447).
2. Ensure the Pinterest module points to your desired Board (e.g. *Quick & Healthy Easy Meals*).
3. Toggle the switch to **ON** (`Active: True`).
4. Make will now check your live `/feed/pinterest.xml` and publish new pins automatically on your chosen schedule!

---

## 3. Autonomous Daily Pipeline (Cron Setup)

To have the server autonomously generate a fresh recipe, render its 1000x1500 pin graphic, compile the site, and update the RSS feed every day at 8:00 AM:

```bash
# Enable the systemd timer for your user account
systemctl --user enable --now /home/hamzazahid8/daily-healthy-meals/config/systemd/pureplated-daily.timer

# Verify the timer is active
systemctl --user list-timers --no-pager | grep pureplated
```

Whenever the timer fires, it executes `scripts/daily_pipeline.py` and appends detailed logs to `scripts/daily_pipeline.log`.

---

## 4. Monetization Expansion Roadmap

Once traffic begins flowing from Pinterest, implement these 3 high-leverage revenue multipliers:

### 1. Amazon Bounty Programs ($3 – $5 Payouts)
* **Amazon Fresh Free Trial:** Embed banners offering a $10 coupon or 30-day free trial on Amazon Fresh grocery delivery.
* **Amazon Prime 30-Day Free Trial:** Target busy parents who want 2-day delivery on glass meal prep containers and cookware.

### 2. High-Ticket Kitchen Appliance Reviews
Write detailed dedicated gear reviews for $150–$400 items:
* *Vitamix 5200 vs Ninja Professional Blender* (High intent, 4% affiliate fee on $350 = $14/sale)
* *Cosori Dual-Basket vs Ninja Air Fryer*
* *Best Glass Meal Prep Containers Tested for Leaks*

### 3. Mediavine / AdThrive Display Ads (At 50k Sessions/Month)
Food and recipe blogs enjoy some of the highest RPMs in the digital publishing industry ($25 to $45 RPM). At 100,000 monthly sessions driven by Pinterest, display ad revenue alone generates $2,500 to $4,500/month, completely passive and on top of Amazon affiliate commissions!
