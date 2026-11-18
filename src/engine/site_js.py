RECIPE_PAGE_JS = """<script>
  // Floating Quick-Action Bar Visibility
  const floatingBar = document.getElementById('floatingBar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 380) {
      floatingBar.classList.add('visible');
    } else {
      floatingBar.classList.remove('visible');
    }
  }, { passive: true });

  // Ingredient Checklist Strikethrough
  function toggleIng(checkbox) {
    const label = checkbox.nextElementSibling;
    if (checkbox.checked) {
      label.classList.add('ing-checked');
    } else {
      label.classList.remove('ing-checked');
    }
  }

  // Step-by-Step Progress Tracking
  function toggleStep(stepEl) {
    stepEl.classList.toggle('step-completed');
    updateProgress();
  }

  function updateProgress() {
    const steps = document.querySelectorAll('.instruction-step');
    const completed = document.querySelectorAll('.instruction-step.step-completed').length;
    const total = steps.length;
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;

    const fill = document.getElementById('progressFill');
    const text = document.getElementById('progressText');
    if (fill) fill.style.width = pct + '%';
    if (text) text.innerText = `${completed} of ${total} steps (${pct}%)`;

    if (completed === total && total > 0) {
      showToast('🎉 All steps complete! Dinner is served.');
    }
  }

  // Dynamic Serving Scaler & Unit Converter
  let currentServingsMult = 1.0;
  let currentUnitMode = 'us';

  const UNIT_CONVERSIONS = {
    'tbsp': { metricUnit: 'ml', factor: 15 },
    'tablespoon': { metricUnit: 'ml', factor: 15 },
    'tablespoons': { metricUnit: 'ml', factor: 15 },
    'tsp': { metricUnit: 'ml', factor: 5 },
    'teaspoon': { metricUnit: 'ml', factor: 5 },
    'teaspoons': { metricUnit: 'ml', factor: 5 },
    'cup': { metricUnit: 'ml', factor: 240 },
    'cups': { metricUnit: 'ml', factor: 240 },
    'oz': { metricUnit: 'g', factor: 28.35 },
    'ounce': { metricUnit: 'g', factor: 28.35 },
    'ounces': { metricUnit: 'g', factor: 28.35 },
    'lb': { metricUnit: 'g', factor: 453.6 },
    'lbs': { metricUnit: 'g', factor: 453.6 },
    'pound': { metricUnit: 'g', factor: 453.6 },
    'pounds': { metricUnit: 'g', factor: 453.6 },
    '6-oz fillets': { metricUnit: '170g fillets', factor: 1 }
  };

  function updateIngredientsDisplay() {
    document.querySelectorAll('.ing-item').forEach(el => {
      const amtEl = el.querySelector('.ing-amt');
      const unitEl = el.querySelector('.ing-unit');
      if (!amtEl) return;

      const baseAmt = parseFloat(amtEl.getAttribute('data-base'));
      const baseUnit = unitEl ? unitEl.getAttribute('data-base-unit') : '';

      amtEl.classList.add('bump');
      setTimeout(() => amtEl.classList.remove('bump'), 220);

      if (isNaN(baseAmt)) return;

      let scaledAmt = baseAmt * currentServingsMult;
      let displayUnit = baseUnit;

      if (currentUnitMode === 'metric' && baseUnit && UNIT_CONVERSIONS[baseUnit.toLowerCase()]) {
        const conv = UNIT_CONVERSIONS[baseUnit.toLowerCase()];
        scaledAmt = scaledAmt * conv.factor;
        displayUnit = conv.metricUnit;
      }

      amtEl.innerText = scaledAmt % 1 === 0 ? scaledAmt.toFixed(0) : scaledAmt.toFixed(1);
      if (unitEl) unitEl.innerText = displayUnit;
    });
  }

  function setServingMultiplier(mult, btn) {
    document.querySelectorAll('.serv-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentServingsMult = mult;
    updateIngredientsDisplay();
    showToast(`Scaled ingredients to ${mult}x servings!`);
  }

  function setUnitSystem(mode, btn) {
    document.querySelectorAll('.unit-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentUnitMode = mode;
    updateIngredientsDisplay();
    showToast(`Units switched to ${mode === 'metric' ? 'Metric (g / ml)' : 'US Customary'}`);
  }

  // Cook Mode (Screen Wake Lock API)
  let wakeLock = null;
  async function toggleCookMode(checkbox) {
    const wrap = document.querySelector('.cook-mode-wrap');
    if (checkbox.checked) {
      try {
        if ('wakeLock' in navigator) {
          wakeLock = await navigator.wakeLock.request('screen');
          wakeLock.addEventListener('release', () => {
            wrap.classList.remove('cook-mode-active');
            checkbox.checked = false;
          });
        }
        wrap.classList.add('cook-mode-active');
        showToast('🍳 Cook Mode Active: Screen will stay awake while you cook!');
      } catch (err) {
        wrap.classList.add('cook-mode-active');
        showToast('🍳 Cook Mode Enabled');
      }
    } else {
      if (wakeLock) {
        await wakeLock.release();
        wakeLock = null;
      }
      wrap.classList.remove('cook-mode-active');
      showToast('Cook Mode turned off');
    }
  }

  // Add to Weekly Meal Plan Sync
  function addToMealPlan(slug, title) {
    try {
      let plan = JSON.parse(localStorage.getItem('cleanplated_meal_plan') || '[]');
      if (!plan.some(item => item.id === slug)) {
        plan.push({ id: slug, title: title, dateAdded: new Date().toISOString() });
        localStorage.setItem('cleanplated_meal_plan', JSON.stringify(plan));
        showToast(`Added "${title}" to your Weekly Meal Plan! 🥗`);
      } else {
        showToast(`"${title}" is already in your Weekly Meal Plan!`);
      }
    } catch (e) {
      showToast(`Added to your Weekly Meal Plan! 🥗`);
    }
  }

  // Native Share / Clipboard Copy
  async function shareRecipe(title, url) {
    if (navigator.share) {
      try {
        await navigator.share({
          title: title + ' | CleanPlated',
          text: 'Check out this 20-minute healthy dinner on CleanPlated:',
          url: url
        });
        return;
      } catch (e) {}
    }
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => {
        showToast('Recipe link copied to clipboard! 📋');
      }).catch(() => {
        showToast('Recipe link ready: ' + url);
      });
    } else {
      showToast('Recipe link ready: ' + url);
    }
  }

  // Toast Notifications
  function showToast(message) {
    let container = document.getElementById('toastContainer');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toastContainer';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast-msg';
    toast.innerHTML = `<span>🌿</span> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 320);
    }, 3200);
  }

  // Scroll Reveal Observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>"""

HOMEPAGE_JS = """<script>
  // Minimalist Baker Style Reactive Live Filter & Search
  const searchInput = document.getElementById('recipeSearchInput');
  const countBadge = document.getElementById('visibleCount');
  const cards = document.querySelectorAll('.recipe-card');
  const noResults = document.getElementById('noResultsMsg');
  let activeTag = 'all';

  function applySearchAndFilter() {
    const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
    let visible = 0;

    cards.forEach(card => {
      const title = (card.querySelector('.card-title') ? card.querySelector('.card-title').innerText : '').toLowerCase();
      const desc = (card.querySelector('.card-desc') ? card.querySelector('.card-desc').innerText : '').toLowerCase();
      const tags = (card.getAttribute('data-tags') || '').toLowerCase();
      const cat = (card.getAttribute('data-category') || '').toLowerCase();

      const matchesQuery = !q || title.includes(q) || desc.includes(q) || tags.includes(q) || cat.includes(q);

      let matchesTag = true;
      if (activeTag === 'under-20') {
        const t = parseInt(card.getAttribute('data-time') || '99');
        matchesTag = t <= 20;
      } else if (activeTag === 'high-protein') {
        const p = parseInt(card.getAttribute('data-protein') || '0');
        matchesTag = p >= 40;
      } else if (activeTag === 'air-fryer') {
        matchesTag = tags.includes('air fryer') || title.includes('air fryer');
      } else if (activeTag === 'low-carb') {
        matchesTag = tags.includes('low-carb') || tags.includes('keto') || tags.includes('bowl');
      } else if (activeTag === 'skillet') {
        matchesTag = tags.includes('skillet') || title.includes('skillet') || tags.includes('one-pan');
      }

      if (matchesQuery && matchesTag) {
        card.style.display = 'flex';
        visible++;
      } else {
        card.style.display = 'none';
      }
    });

    if (countBadge) {
      countBadge.innerText = `Showing ${visible} healthy recipe${visible === 1 ? '' : 's'}`;
    }
    if (noResults) {
      noResults.style.display = visible === 0 ? 'block' : 'none';
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', applySearchAndFilter);
  }

  window.filterByChip = function(tag, btn) {
    document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeTag = tag;
    applySearchAndFilter();
  };

  window.resetSearch = function() {
    if (searchInput) searchInput.value = '';
    const allBtn = document.querySelector('.filter-chip[data-tag="all"]');
    if (allBtn) {
      document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
      allBtn.classList.add('active');
    }
    activeTag = 'all';
    applySearchAndFilter();
  };

  // Scroll-Triggered Reveal Animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>"""
