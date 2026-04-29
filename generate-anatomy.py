#!/usr/bin/env python3
"""Generate 4 anatomy & physiology deck HTML pages and update catalog.json."""
import json, html, os, sys

SITE = "/Users/stephaniedugas/Documents/stacked-site"

# Load card data from extracted temp file
exec(open("/tmp/anatomy_cards_raw.py").read())

# --- Apply corrections ---
# 1. Triceps card: fix "Only elbow extensor"
for i, (front, back) in enumerate(SKELETAL_MUSCULAR):
    if "Triceps brachii" in front:
        SKELETAL_MUSCULAR[i] = (front, back.replace(
            "Only elbow extensor",
            "Primary elbow extensor (anconeus also assists)"
        ))
        print(f"[CORRECTION] Triceps card updated at index {i}")
        break

# 2. Small intestine surface area: fix ~600x (~200 m²)
for i, (front, back) in enumerate(DIGESTIVE_ENDOCRINE):
    if "surface area" in front.lower() or "~600x" in back or "~200 m" in back:
        DIGESTIVE_ENDOCRINE[i] = (front, back.replace(
            "~600x (~200 m²)",
            "greatly increased (historically cited as ~200 m², more recent estimates suggest ~32 m²)"
        ))
        print(f"[CORRECTION] Surface area card updated at index {i}")
        break

DECKS = [
    {
        "slug": "anatomy-skeletal-muscular",
        "title": "Anatomy: Skeletal & Muscular System",
        "category": "College",
        "description": "Comprehensive flashcards covering bone classification, major bones, joint types, muscle actions, sliding filament theory, and common injuries.",
        "meta_desc": "Free Anatomy & Physiology flashcards: Skeletal & Muscular System. Study bones, joints, muscles, and more online or import into Stacked.",
        "keywords": "anatomy flashcards, skeletal system, muscular system, bones, joints, muscles, A&P study cards",
        "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
        "cards": SKELETAL_MUSCULAR,
    },
    {
        "slug": "anatomy-cardiovascular-respiratory",
        "title": "Anatomy: Cardiovascular & Respiratory",
        "category": "College",
        "description": "Comprehensive flashcards covering heart anatomy, cardiac cycle, blood vessels, blood composition, respiratory anatomy, gas exchange, and lung volumes.",
        "meta_desc": "Free Anatomy & Physiology flashcards: Cardiovascular & Respiratory System. Study heart, blood vessels, lungs, and gas exchange.",
        "keywords": "anatomy flashcards, cardiovascular system, respiratory system, heart, lungs, blood, A&P study cards",
        "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
        "cards": CARDIOVASCULAR_RESPIRATORY,
    },
    {
        "slug": "anatomy-nervous-system",
        "title": "Anatomy: Nervous System & Brain",
        "category": "College",
        "description": "Comprehensive flashcards covering neuron structure, action potentials, neurotransmitters, brain regions, cranial nerves, and autonomic nervous system.",
        "meta_desc": "Free Anatomy & Physiology flashcards: Nervous System & Brain. Study neurons, brain anatomy, cranial nerves, and more.",
        "keywords": "anatomy flashcards, nervous system, brain anatomy, cranial nerves, neurotransmitters, A&P study cards",
        "color": {"hex": "#AF52DE", "r": 0.686, "g": 0.322, "b": 0.969},
        "cards": NERVOUS_SYSTEM,
    },
    {
        "slug": "anatomy-digestive-endocrine",
        "title": "Anatomy: Digestive & Endocrine",
        "category": "College",
        "description": "Comprehensive flashcards covering GI tract organs, digestive enzymes, liver functions, endocrine glands, hormones, and feedback loops.",
        "meta_desc": "Free Anatomy & Physiology flashcards: Digestive & Endocrine System. Study GI tract, hormones, glands, and metabolism.",
        "keywords": "anatomy flashcards, digestive system, endocrine system, hormones, GI tract, A&P study cards",
        "color": {"hex": "#30D158", "r": 0.188, "g": 0.820, "b": 0.345},
        "cards": DIGESTIVE_ENDOCRINE,
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page_title} | Stacked</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="https://stackedflashcards.com/decks/{slug}.html" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://stackedflashcards.com/decks/{slug}.html" />
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:image" content="https://stackedflashcards.com/og-image.png" />
  <meta property="og:site_name" content="Stacked Flashcards" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{page_title}" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="https://stackedflashcards.com/og-image.png" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LearningResource",
    "name": "{title}",
    "description": "{description}",
    "educationalLevel": "Beginner",
    "learningResourceType": "Flashcards",
    "isAccessibleForFree": true,
    "url": "https://stackedflashcards.com/decks/{slug}.html",
    "provider": {{ "@type": "Organization", "name": "Stacked Flashcards", "url": "https://stackedflashcards.com" }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://stackedflashcards.com/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Decks", "item": "https://stackedflashcards.com/decks.html" }},
      {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "https://stackedflashcards.com/decks/{slug}.html" }}
    ]
  }}
  </script>
  <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"></script>
  <link rel="icon" href="/favicon.ico" sizes="32x32" />
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/manifest.json" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--purple:#a855f7;--blue:#3b82f6;--bg-primary:#09090b;--bg-secondary:#0f0f12;--bg-card:#16161a;--border:#1e1e24;--border-hover:#2e2e38;--text-primary:#f4f4f5;--text-secondary:#a1a1aa;--text-muted:#52525b;--gradient:linear-gradient(135deg,#a855f7,#6366f1,#3b82f6);--gradient-subtle:linear-gradient(135deg,rgba(168,85,247,0.12),rgba(59,130,246,0.12));--glow-purple:rgba(168,85,247,0.15);--radius:16px;--radius-sm:10px;--radius-lg:24px}}
    html{{scroll-behavior:smooth}}
    body{{background:var(--bg-primary);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:var(--text-primary);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
    body::before{{content:'';position:fixed;inset:0;background:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");pointer-events:none;z-index:1}}
    nav{{position:sticky;top:0;z-index:1000;background:rgba(9,9,11,0.8);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);border-bottom:1px solid rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:space-between;padding:0 32px;height:64px}}
    .nav-logo{{font-size:1.2rem;font-weight:800;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none;letter-spacing:-0.02em}}
    .nav-links{{display:flex;gap:4px;align-items:center}}
    .nav-links a{{color:var(--text-muted);text-decoration:none;font-size:0.875rem;font-weight:500;padding:8px 14px;border-radius:var(--radius-sm);transition:all 0.2s ease}}
    .nav-links a:hover{{color:var(--text-primary);background:rgba(255,255,255,0.05)}}
    .nav-cta{{background:var(--gradient)!important;color:white!important;padding:8px 18px!important;border-radius:var(--radius-sm)!important;font-weight:600!important;font-size:0.85rem!important}}
    .nav-cta:hover{{opacity:0.9!important}}
    main{{max-width:720px;margin:0 auto;padding:48px 24px 80px}}
    .page-header{{text-align:center;margin-bottom:40px;position:relative}}
    .page-header::before{{content:'';position:absolute;top:-100px;left:50%;transform:translateX(-50%);width:500px;height:300px;background:radial-gradient(ellipse,var(--glow-purple) 0%,transparent 70%);pointer-events:none;z-index:0}}
    .page-header>*{{position:relative;z-index:1}}
    .page-badge{{display:inline-flex;align-items:center;gap:6px;background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.2);color:#4ade80;font-size:0.72rem;font-weight:700;padding:5px 14px;border-radius:100px;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.06em}}
    .cat-badge{{background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);color:var(--purple);margin-right:8px}}
    .page-header h1{{font-size:clamp(1.8rem,4vw,2.4rem);font-weight:900;letter-spacing:-0.03em;margin-bottom:10px;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
    .page-desc{{color:var(--text-secondary);font-size:1rem;line-height:1.6;max-width:560px;margin:0 auto 24px}}
    .deck-stats{{display:flex;gap:24px;justify-content:center;margin-bottom:32px;font-size:0.82rem;color:var(--text-muted)}}
    .deck-stats span{{font-weight:600;color:var(--text-secondary)}}
    .import-bar{{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px;margin-bottom:40px;text-align:center}}
    .import-bar p{{color:var(--text-secondary);font-size:0.92rem;margin-bottom:16px}}
    .btn-import{{display:inline-block;background:var(--gradient);color:white;padding:14px 32px;border-radius:14px;text-decoration:none;font-weight:700;font-size:1rem;border:none;cursor:pointer;font-family:inherit;transition:opacity 0.2s,transform 0.2s;box-shadow:0 4px 20px rgba(168,85,247,0.25)}}
    .btn-import:hover{{opacity:0.9;transform:translateY(-2px)}}
    .btn-secondary{{display:inline-block;background:rgba(255,255,255,0.05);color:var(--text-secondary);border:1px solid var(--border);padding:10px 20px;border-radius:var(--radius-sm);text-decoration:none;font-weight:600;font-size:0.85rem;margin-left:10px;cursor:pointer;font-family:inherit;transition:all 0.2s}}
    .btn-secondary:hover{{border-color:var(--border-hover);color:var(--text-primary)}}
    #qrcode{{display:none;justify-content:center;margin-top:16px}}
    #qrcode canvas{{border-radius:var(--radius-sm)}}
    .cards-section h2{{font-size:1.2rem;font-weight:700;margin-bottom:20px;color:var(--text-primary)}}
    .card-list{{display:flex;flex-direction:column;gap:8px}}
    .card-item{{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px 18px;display:grid;grid-template-columns:1fr 1fr;gap:16px;transition:border-color 0.2s}}
    .card-item:hover{{border-color:var(--border-hover)}}
    .card-front{{font-weight:600;font-size:0.9rem;color:var(--text-primary)}}
    .card-back{{font-size:0.88rem;color:var(--text-muted);line-height:1.5}}
    .card-divider{{width:1px;background:var(--border)}}
    .app-cta{{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:32px 24px;margin-top:48px;text-align:center;position:relative;overflow:hidden}}
    .app-cta::before{{content:'';position:absolute;inset:0;background:var(--gradient-subtle);opacity:0.5}}
    .app-cta>*{{position:relative;z-index:1}}
    .app-cta p{{color:var(--text-secondary);font-size:1rem;margin-bottom:16px;line-height:1.6}}
    .app-cta .g{{background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700}}
    .app-cta a{{display:inline-block;background:var(--gradient);color:white;padding:13px 28px;border-radius:14px;text-decoration:none;font-weight:600;font-size:0.95rem;transition:opacity 0.2s}}
    .app-cta a:hover{{opacity:0.9}}
    footer{{padding:40px 24px;border-top:1px solid var(--border)}}
    .footer-inner{{max-width:740px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}}
    .footer-brand{{font-size:1rem;font-weight:800;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
    .footer-links{{display:flex;gap:24px;flex-wrap:wrap}}
    .footer-links a{{color:var(--text-muted);text-decoration:none;font-size:0.82rem;font-weight:500;transition:color 0.2s}}
    .footer-links a:hover{{color:var(--text-secondary)}}
    .footer-copy{{width:100%;text-align:center;margin-top:24px;font-size:0.75rem;color:var(--text-muted)}}
    @media(max-width:640px){{nav{{padding:0 16px}}.nav-links a:not(.nav-cta){{display:none}}main{{padding:32px 16px 60px}}.card-item{{grid-template-columns:1fr;gap:6px}}.footer-inner{{justify-content:center;text-align:center}}.footer-links{{justify-content:center}}}}
  </style>
</head>
<body>
  <nav>
    <a class="nav-logo" href="/">Stacked</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/decks.html">Decks</a>
      <a href="/timer.html">Timer</a>
      <a href="https://apps.apple.com/app/id6744585549" target="_blank" rel="noopener" class="nav-cta">Download Free</a>
    </div>
  </nav>

  <main>
    <div class="page-header">
      <span class="page-badge cat-badge">{category}</span>
      <span class="page-badge">{card_count} Cards — Free</span>
      <h1>{title}</h1>
      <p class="page-desc">{description}</p>
    </div>

    <div class="import-bar">
      <p>Import this deck directly into the Stacked app</p>
      <button class="btn-import" onclick="importDeck()">Import to Stacked</button>
      <button class="btn-secondary" onclick="toggleQR()">Show QR Code</button>
      <div id="qrcode"></div>
    </div>

    <div class="cards-section">
      <h2>All {card_count} Cards</h2>
      <div class="card-list">
{card_html}
      </div>
    </div>

    <div class="app-cta">
      <p>Study this deck on the go with <span class="g">Stacked</span> — the AI-powered flashcard app.</p>
      <a href="https://apps.apple.com/app/id6744585549" target="_blank" rel="noopener">Get Stacked Free →</a>
    </div>
  </main>

  <footer>
    <div class="footer-inner">
      <div class="footer-brand">Stacked</div>
      <div class="footer-links">
        <a href="/">Home</a>
        <a href="/decks.html">Browse Decks</a>
        <a href="/timer.html">Pomodoro Timer</a>
        <a href="/privacy.html">Privacy Policy</a>
      </div>
      <div class="footer-copy">&copy; 2025 Stacked Flashcards. All rights reserved.</div>
    </div>
  </footer>

  <script>
    const deckData = {deck_json};

    function importDeck() {{
      const stack = {{
        id: crypto.randomUUID(),
        title: deckData.title,
        cards: deckData.cards.map(c => ({{ id: crypto.randomUUID(), front: c[0], back: c[1] }})),
        color: deckData.color
      }};
      const json = JSON.stringify(stack);
      const utf8Bytes = new TextEncoder().encode(json);
      let binary = '';
      for (let i = 0; i < utf8Bytes.length; i++) binary += String.fromCharCode(utf8Bytes[i]);
      const encoded = btoa(binary);
      window.location.href = 'https://stackedflashcards.com/import?stack=' + encodeURIComponent(encoded);
    }}

    function toggleQR() {{
      const qr = document.getElementById('qrcode');
      if (qr.style.display === 'flex') {{ qr.style.display = 'none'; return; }}
      const stack = {{
        id: crypto.randomUUID(),
        title: deckData.title,
        cards: deckData.cards.map(c => ({{ id: crypto.randomUUID(), front: c[0], back: c[1] }})),
        color: deckData.color
      }};
      const json = JSON.stringify(stack);
      const utf8Bytes = new TextEncoder().encode(json);
      let binary = '';
      for (let i = 0; i < utf8Bytes.length; i++) binary += String.fromCharCode(utf8Bytes[i]);
      const encoded = btoa(binary);
      const link = 'https://stackedflashcards.com/import?stack=' + encodeURIComponent(encoded);
      qr.innerHTML = '';
      QRCode.toCanvas(link, {{ width: 200, margin: 2, color: {{ dark: '#000', light: '#fff' }} }}, (err, canvas) => {{
        if (!err) qr.appendChild(canvas);
      }});
      qr.style.display = 'flex';
    }}
  </script>
</body>
</html>"""

# Generate all deck pages
for deck in DECKS:
    card_html_lines = []
    for front, back in deck["cards"]:
        f = html.escape(front)
        b = html.escape(back)
        card_html_lines.append(f'        <div class="card-item"><div class="card-front">{f}</div><div class="card-back">{b}</div></div>')

    card_html = "\n".join(card_html_lines)

    deck_json = json.dumps({
        "title": deck["title"],
        "cards": deck["cards"],
        "color": {"red": deck["color"]["r"], "green": deck["color"]["g"], "blue": deck["color"]["b"]}
    })

    page_title = f"Free {deck['title']} Flashcards"

    page = TEMPLATE.format(
        page_title=page_title,
        meta_desc=deck["meta_desc"],
        keywords=deck["keywords"],
        slug=deck["slug"],
        title=deck["title"],
        description=deck["description"],
        category=deck["category"],
        card_count=len(deck["cards"]),
        card_html=card_html,
        deck_json=deck_json,
    )

    filepath = os.path.join(SITE, "decks", f"{deck['slug']}.html")
    with open(filepath, "w") as f:
        f.write(page)
    print(f"SUCCESS: {deck['slug']}.html ({len(deck['cards'])} cards)")

print(f"\nGenerated {len(DECKS)} anatomy deck pages")

# Update catalog.json — load existing, append new entries
catalog_path = os.path.join(SITE, "decks", "catalog.json")
with open(catalog_path, "r") as f:
    catalog = json.load(f)

# Remove any existing anatomy deck entries (by slug) to avoid duplicates
new_slugs = {d["slug"] for d in DECKS}
catalog = [entry for entry in catalog if entry["slug"] not in new_slugs]

# Append new entries
for d in DECKS:
    catalog.append({
        "slug": d["slug"],
        "title": d["title"],
        "category": d["category"],
        "description": d["description"],
        "card_count": len(d["cards"]),
        "color": d["color"]["hex"],
    })

with open(catalog_path, "w") as f:
    json.dump(catalog, f, indent=2)
print("SUCCESS: catalog.json updated with 4 new anatomy decks")
