#!/usr/bin/env python3
"""Apply cross-cutting fixes across all HTML pages."""
import os, glob, re

SITE = "/Users/stephaniedugas/Documents/stacked-site"

# Collect all HTML files
html_files = glob.glob(os.path.join(SITE, "*.html")) + glob.glob(os.path.join(SITE, "decks", "*.html"))
print(f"Found {len(html_files)} HTML files\n")

# ── Fix #5: Copyright 2025 → 2026 ──
count = 0
for f in html_files:
    with open(f, 'r') as fh:
        content = fh.read()
    if '© 2025' in content or '&copy; 2025' in content:
        content = content.replace('© 2025', '© 2026').replace('&copy; 2025', '&copy; 2026')
        with open(f, 'w') as fh:
            fh.write(content)
        count += 1
print(f"✅ Fix #5: Copyright updated to 2026 in {count} files")

# ── Fix #6: Add hamburger menu CSS + HTML + JS ──
# CSS to add inside existing <style> block
HAMBURGER_CSS = """
    /* ── Hamburger menu ── */
    .nav-hamburger {
      display: none;
      flex-direction: column;
      gap: 5px;
      background: none;
      border: none;
      cursor: pointer;
      padding: 8px;
      z-index: 1002;
    }
    .nav-hamburger span {
      display: block;
      width: 20px;
      height: 2px;
      background: var(--text-secondary, #a1a1aa);
      border-radius: 2px;
      transition: all 0.3s;
    }
    .nav-mobile {
      display: none;
      position: fixed;
      inset: 0;
      top: 64px;
      background: rgba(9, 9, 11, 0.98);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      flex-direction: column;
      align-items: center;
      padding: 40px 24px;
      gap: 8px;
      z-index: 999;
    }
    .nav-mobile.open { display: flex; }
    .nav-mobile a {
      color: #a1a1aa;
      text-decoration: none;
      font-size: 1.1rem;
      font-weight: 600;
      padding: 14px 24px;
      border-radius: 12px;
      transition: all 0.2s;
      width: 100%;
      max-width: 320px;
      text-align: center;
    }
    .nav-mobile a:hover { color: #f4f4f5; background: rgba(255,255,255,0.05); }
    .nav-mobile .mobile-cta {
      background: linear-gradient(135deg, #a855f7, #6366f1, #3b82f6);
      color: white;
      margin-top: 8px;
    }
"""

HAMBURGER_MEDIA_ADDITIONS = """      .nav-hamburger { display: flex; }"""

# HTML to add inside nav, after nav-links div
HAMBURGER_HTML = """    <button class="nav-hamburger" onclick="document.querySelector('.nav-mobile').classList.toggle('open')" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>"""

MOBILE_MENU_HTML = """
  <div class="nav-mobile">
    <a href="/">Home</a>
    <a href="/decks.html">Browse Decks</a>
    <a href="/timer.html">Pomodoro Timer</a>
    <a href="/import.html">Flashcard Maker</a>
    <a href="/study-tips.html">Study Tips</a>
    <a href="/grade-calculator.html">Grade Calculator</a>
    <a href="https://apps.apple.com/app/id6744585549" target="_blank" rel="noopener" class="mobile-cta">Download Free</a>
  </div>"""

count = 0
for f in html_files:
    with open(f, 'r') as fh:
        content = fh.read()

    if 'nav-hamburger' in content:
        continue  # Already has hamburger

    # 1. Add hamburger CSS before the closing </style>
    # Find the last occurrence of the mobile media query
    if '@media' in content and 'nav-hamburger' not in content:
        # Add hamburger CSS just before the closing </style>
        content = content.replace('  </style>', HAMBURGER_CSS + '  </style>')

        # Add .nav-hamburger { display: flex; } inside the @media block
        # Find the mobile @media rule and add to it
        # Look for the pattern: .nav-links a:not(.nav-cta) { display: none; }
        content = content.replace(
            '.nav-links a:not(.nav-cta) { display: none; }',
            '.nav-links a:not(.nav-cta) { display: none; }\n' + HAMBURGER_MEDIA_ADDITIONS
        )

    # 2. Add hamburger button inside nav, after </div> (nav-links)
    content = content.replace(
        '    </div>\n  </nav>',
        '    </div>\n' + HAMBURGER_HTML + '\n  </nav>\n' + MOBILE_MENU_HTML
    )

    with open(f, 'w') as fh:
        fh.write(content)
    count += 1

print(f"✅ Fix #6: Hamburger menu added to {count} files")

# ── Fix #11: Standardize footer links ──
# Standard footer: Home, Browse Decks, Pomodoro Timer, Flashcard Maker, Privacy Policy
STANDARD_FOOTER_LINKS = """      <div class="footer-links">
        <a href="/">Home</a>
        <a href="/decks.html">Browse Decks</a>
        <a href="/timer.html">Pomodoro Timer</a>
        <a href="/import.html">Flashcard Maker</a>
        <a href="/privacy.html">Privacy Policy</a>
      </div>"""

count = 0
for f in html_files:
    with open(f, 'r') as fh:
        content = fh.read()

    # Replace footer-links div with standard version
    pattern = r'<div class="footer-links">.*?</div>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        old = match.group(0)
        new = STANDARD_FOOTER_LINKS.strip()
        if old.strip() != new.strip():
            content = content[:match.start()] + new + content[match.end():]
            with open(f, 'w') as fh:
                fh.write(content)
            count += 1

print(f"✅ Fix #11: Footer standardized in {count} files")

print("\n🎉 All cross-cutting fixes applied!")
