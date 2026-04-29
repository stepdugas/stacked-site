#!/usr/bin/env python3
"""Generate nursing-lab-values.html deck page."""
import json, html, os

SITE = "/Users/stephaniedugas/Documents/stacked-site"

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

# All 50 cards for Deck 5: Lab Values & Vital Signs
# With corrections applied:
# 1. Magnesium: "1.8-3.0 mg/dL" -> "1.8-2.4 mg/dL"
# 2. Potassium critical value: ">6.5 mEq/L" -> ">6.0 mEq/L" in the critical values card
# 3. Hemoglobin transfusion: clarified guidance

CARDS = [
    # 1 - Sodium
    ("Sodium (Na+): Normal range and clinical significance?",
     "Normal: 136-145 mEq/L. Hyponatremia (<136): causes \u2014 SIADH, water intoxication, diuretics, heart failure, vomiting/diarrhea. Symptoms: confusion, headache, nausea, seizures (severe <120). Correct slowly (<8-12 mEq/L per 24 hrs \u2014 rapid correction \u2192 osmotic demyelination syndrome/central pontine myelinolysis). Hypernatremia (>145): causes \u2014 dehydration, diabetes insipidus, excessive sodium intake. Symptoms: thirst, dry mucous membranes, restlessness, seizures. Correct slowly (reduce no more than 10-12 mEq/L per 24 hrs \u2014 rapid correction \u2192 cerebral edema)."),

    # 2 - Potassium
    ("Potassium (K+): Normal range, hypo/hyperkalemia signs and ECG changes?",
     "Normal: 3.5-5.0 mEq/L. Hypokalemia (<3.5): causes \u2014 diuretics (loop, thiazide), vomiting, diarrhea, alkalosis. Symptoms: muscle weakness, leg cramps, fatigue, decreased bowel sounds, shallow respirations. ECG: flattened T waves, ST depression, U waves, prolonged QT. Increases digoxin toxicity risk. Hyperkalemia (>5.0): causes \u2014 renal failure, ACE inhibitors, K+-sparing diuretics, acidosis, tissue destruction (burns, crush injury). Symptoms: muscle weakness, paresthesias, bradycardia, cardiac arrest. ECG: tall peaked T waves, widened QRS, prolonged PR, sine wave \u2192 Vfib. CRITICAL VALUE: >6.0 mEq/L. Treatment: calcium gluconate (cardiac membrane stabilizer \u2014 first), insulin + D50 (shifts K+ into cells), sodium bicarb, kayexalate/patiromer (GI elimination), albuterol nebulizer, dialysis."),

    # 3 - Chloride
    ("Chloride (Cl-): Normal range and when is it abnormal?",
     "Normal: 98-106 mEq/L. Follows sodium \u2014 usually changes in same direction. Hypochloremia (<98): causes \u2014 vomiting, NG suctioning (loss of HCl), metabolic alkalosis, diuretics, SIADH. Hyperchloremia (>106): causes \u2014 dehydration, renal tubular acidosis, excessive NS infusion, metabolic acidosis (non-anion gap). Chloride helps maintain acid-base balance and electrical neutrality. Assess in context of sodium and bicarbonate levels."),

    # 4 - CO2/Bicarbonate
    ("CO2 (Bicarbonate/HCO3): Normal range and acid-base significance?",
     "Normal: 22-26 mEq/L (venous CO2 on BMP represents bicarbonate). HCO3 is a BASE \u2014 regulated by kidneys. Low HCO3 (<22) = metabolic acidosis (DKA, lactic acidosis, renal failure, severe diarrhea). High HCO3 (>26) = metabolic alkalosis (vomiting, NG suction, excessive antacids, hypokalemia). Kidneys compensate for respiratory disorders by retaining or excreting HCO3 (takes 24-48 hrs). On ABG: HCO3 22-26 mEq/L. If metabolic acidosis: calculate anion gap = Na - (Cl + HCO3); normal 8-12. Elevated anion gap = MUDPILES causes."),

    # 5 - BUN
    ("BUN (Blood Urea Nitrogen): Normal range and clinical significance?",
     "Normal: 10-20 mg/dL. Measures urea \u2014 end product of protein metabolism cleared by kidneys. Elevated (azotemia): prerenal (dehydration, heart failure, shock, GI bleeding, high protein diet), renal (kidney disease, nephrotoxic drugs), postrenal (obstruction). Decreased: liver failure (can't produce urea), malnutrition, overhydration. BUN/Creatinine ratio: normally 10:1 to 20:1. Elevated ratio (>20:1): suggests prerenal cause (dehydration, GI bleed). Normal ratio with both elevated: intrinsic renal disease. Always interpret BUN with creatinine. Affected by protein intake, hydration status, GI bleeding."),

    # 6 - Creatinine
    ("Creatinine: Normal range and why is it more reliable than BUN?",
     "Normal: 0.7-1.3 mg/dL (male), 0.6-1.1 mg/dL (female). Byproduct of muscle metabolism \u2014 reflects GFR more accurately than BUN because it is NOT affected by protein intake, hydration, or GI bleeding. Elevated creatinine = decreased kidney function. Even small increases are significant (doubling = 50% loss of renal function). eGFR calculated from creatinine, age, sex, race: normal >90 mL/min. CKD staging: Stage 1: eGFR >90 + kidney damage, Stage 2: 60-89, Stage 3a: 45-59, Stage 3b: 30-44, Stage 4: 15-29, Stage 5 (ESRD): <15. Notify provider for acute rise in creatinine (acute kidney injury)."),

    # 7 - Glucose
    ("Glucose: Normal ranges (fasting, random, critical values)?",
     "Fasting: 70-100 mg/dL. Random: 70-140 mg/dL. Pre-diabetes (fasting): 100-125 mg/dL. Diabetes diagnosis: fasting \u2265126 mg/dL (two occasions) or random \u2265200 with symptoms or A1C \u226565%. Hypoglycemia: <70 mg/dL \u2014 shakiness, diaphoresis, confusion, tachycardia, irritability, pallor. Severe <54 mg/dL. Treatment: Rule of 15 \u2014 15g fast-acting carbs (4 oz juice, glucose tabs), recheck in 15 min. If unconscious: glucagon 1 mg IM/SubQ or D50 25 mL IV push. Hyperglycemia: DKA >250-300 with ketosis (Type 1), HHS >600 with severe dehydration (Type 2). Critical values: <40 or >500 mg/dL \u2014 notify provider immediately."),

    # 8 - Calcium
    ("Calcium (Ca2+): Normal range, hypo/hypercalcemia signs?",
     "Total calcium: 9.0-10.5 mg/dL. Ionized calcium: 4.5-5.6 mg/dL (more accurate \u2014 not affected by albumin). Hypocalcemia (<9.0): causes \u2014 hypoparathyroidism, vitamin D deficiency, chronic kidney disease, acute pancreatitis, massive blood transfusion (citrate binds Ca). Symptoms: numbness/tingling (perioral, fingers), muscle cramps, tetany, Chvostek sign (facial twitching with tap), Trousseau sign (carpopedal spasm with BP cuff), laryngospasm, seizures, prolonged QT \u2192 cardiac arrest. Hypercalcemia (>10.5): causes \u2014 hyperparathyroidism (#1), malignancy, immobility, thiazide diuretics. Symptoms: 'bones, stones, groans, moans' \u2014 bone pain, kidney stones, abdominal pain/constipation, confusion/lethargy. ECG: shortened QT. Treatment: IV NS hydration, loop diuretics (furosemide \u2014 promotes Ca excretion), calcitonin, bisphosphonates. Correct calcium for low albumin: add 0.8 mg/dL for every 1 g/dL albumin below 4."),

    # 9 - Magnesium (CORRECTED: 1.8-3.0 -> 1.8-2.4 mg/dL)
    ("Magnesium (Mg2+): Normal range and clinical significance?",
     "Normal: 1.5-2.5 mEq/L (or 1.8-2.4 mg/dL). Hypomagnesemia (<1.5): causes \u2014 alcoholism, malnutrition, diarrhea, PPIs (long-term), diuretics, DKA. Symptoms mirror hypocalcemia: tremors, hyperreflexia, tetany, seizures, cardiac arrhythmias (torsades de pointes), Chvostek/Trousseau positive. KEY: must correct Mg before K+ will correct (refractory hypokalemia). Hypermagnesemia (>2.5): causes \u2014 renal failure, excessive Mg administration (antacids, laxatives, Mg sulfate infusion). Symptoms: decreased DTRs (first sign), lethargy, hypotension, respiratory depression, cardiac arrest. Antidote: calcium gluconate. Monitor in patients on mag sulfate drip (preeclampsia)."),

    # 10 - Phosphorus
    ("Phosphorus: Normal range and its relationship to calcium?",
     "Normal: 2.5-4.5 mg/dL (adult), 4.0-7.0 mg/dL (children \u2014 higher due to growth). Inverse relationship with calcium \u2014 when one rises, the other falls. Hypophosphatemia (<2.5): causes \u2014 refeeding syndrome (most dangerous), alcoholism, DKA treatment (insulin drives phosphorus into cells), antacids (bind phosphorus). Symptoms: muscle weakness, respiratory failure, confusion, rhabdomyolysis, impaired WBC function. Hyperphosphatemia (>4.5): causes \u2014 renal failure (#1), hypoparathyroidism, tumor lysis syndrome, excessive intake. Causes reciprocal hypocalcemia \u2192 tetany, calcification of soft tissues. Treatment: phosphate binders (calcium carbonate, sevelamer) with meals, dietary restriction, dialysis."),

    # 11 - WBC
    ("WBC (White Blood Cell Count): Normal range and differential?",
     "Normal WBC: 4,500-11,000/mm\u00b3 (4.5-11.0 \u00d7 10\u2079/L). Leukocytosis (>11,000): infection, inflammation, stress response, corticosteroids, leukemia. Leukopenia (<4,500): bone marrow suppression (chemo), viral infections, autoimmune disorders, overwhelming sepsis. Differential (mnemonic: Never Let Monkeys Eat Bananas): Neutrophils 55-70% (bacterial infection, first responders \u2014 'left shift' = increased bands/immature neutrophils, indicates acute infection), Lymphocytes 20-40% (viral infection, chronic infection, immune response), Monocytes 2-8% (chronic inflammation), Eosinophils 1-4% (allergies, parasitic infections), Basophils 0.5-1% (allergic reactions, inflammation). Neutropenia: ANC <1500 \u2014 infection risk. ANC <500: severe \u2014 institute neutropenic precautions (private room, no fresh flowers/fruits, hand hygiene, avoid crowds, no rectal temps)."),

    # 12 - RBC/Hemoglobin/Hematocrit (CORRECTED: transfusion guidance clarified)
    ("RBC, Hemoglobin, and Hematocrit: Normal ranges and clinical significance?",
     "RBC: Male 4.7-6.1 million/mm\u00b3, Female 4.2-5.4 million/mm\u00b3. Hemoglobin (carries O2): Male 14-18 g/dL, Female 12-16 g/dL. Hematocrit (% of blood that is RBCs): Male 42-52%, Female 37-47%. Hgb roughly = Hct \u00f7 3. Decreased (anemia): blood loss, iron deficiency, chronic disease, B12/folate deficiency, bone marrow failure. Symptoms: fatigue, pallor, tachycardia, dyspnea, dizziness. Transfuse when Hgb <7 g/dL (stable patients) or <8 g/dL (cardiac disease); also transfuse if symptomatic at higher levels \u2014 each unit raises Hgb ~1 g/dL. Increased (polycythemia): dehydration (relative), polycythemia vera, chronic hypoxia (COPD, high altitude), smoking. Risk: thrombosis. Critical values: Hgb <7 or >20 g/dL \u2014 notify provider."),

    # 13 - Platelets
    ("Platelets: Normal range and clinical significance?",
     "Normal: 150,000-400,000/mm\u00b3. Thrombocytopenia (<150,000): causes \u2014 HIT, ITP, TTP, DIC, chemo, aplastic anemia, liver disease. Bleeding risk increases as count drops: <50,000 \u2014 bleeding with procedures; <20,000 \u2014 spontaneous bleeding risk; <10,000 \u2014 spontaneous hemorrhage risk (transfuse platelets). Signs: petechiae, purpura, ecchymoses, bleeding gums, epistaxis, melena, hematuria. Nursing: fall prevention, soft toothbrush, no razors (electric only), avoid IM injections, no rectal temps, hold pressure on puncture sites, avoid aspirin/NSAIDs. Thrombocytosis (>400,000): reactive (infection, iron deficiency, post-splenectomy) or primary (myeloproliferative disorder). Risk: thrombosis."),

    # 14 - PT/INR
    ("PT/INR: Normal values, therapeutic ranges, and clinical use?",
     "PT (Prothrombin Time): 11-13.5 seconds. Measures extrinsic pathway (factors I, II, V, VII, X). INR (International Normalized Ratio): standardized PT ratio. Normal INR: 0.8-1.1. Therapeutic INR for warfarin: 2.0-3.0 (DVT, PE, afib); 2.5-3.5 (mechanical heart valve). INR >4.0: high bleeding risk. INR >5.0: hold warfarin, consider vitamin K. PT/INR monitors WARFARIN therapy. Elevated PT/INR: liver disease (liver makes clotting factors), DIC, vitamin K deficiency, warfarin therapy. Nursing: consistent vitamin K intake while on warfarin, monitor for bleeding (gums, bruising, dark stools, hematuria), avoid interactions (cranberry, alcohol, many drugs)."),

    # 15 - aPTT
    ("aPTT: Normal value, therapeutic range, and clinical use?",
     "Normal aPTT: 25-35 seconds (varies by lab). Measures intrinsic pathway (factors I, II, V, VIII, IX, X, XI, XII). Monitors HEPARIN (unfractionated) therapy. Therapeutic aPTT: 1.5-2.5\u00d7 control (typically 46-70 seconds). Elevated aPTT: heparin therapy, hemophilia (factor VIII or IX deficiency), DIC, liver disease, von Willebrand disease. If aPTT >100 seconds: high bleeding risk \u2014 hold heparin, notify provider. Antidote: protamine sulfate. Draw aPTT 6 hours after dose change and adjust per protocol. Do NOT use aPTT to monitor LMWH (enoxaparin) \u2014 use anti-Xa level if monitoring needed."),

    # 16 - Fibrinogen
    ("Fibrinogen: Normal range and when is it clinically important?",
     "Normal: 200-400 mg/dL. Fibrinogen (Factor I) is converted to fibrin for clot formation. Decreased (<200): DIC (consumed in widespread clotting), severe liver disease, massive transfusion (dilution), fibrinolytic therapy. DIC: fibrinogen critically low + elevated D-dimer + elevated PT/aPTT + low platelets + microangiopathic hemolytic anemia (schistocytes). Increased (>400): acute inflammation (acute phase reactant), infection, pregnancy, malignancy. Treatment of low fibrinogen: cryoprecipitate (rich in fibrinogen, factor VIII, vWF). Critical value: <100 mg/dL \u2014 significant hemorrhage risk."),

    # 17 - ALT/AST
    ("ALT and AST: Normal ranges and clinical significance?",
     "ALT (Alanine Aminotransferase): 7-56 U/L. More specific to liver. AST (Aspartate Aminotransferase): 10-40 U/L. Found in liver, heart, muscle, kidneys. Elevated: hepatitis (viral, alcoholic, drug-induced), cirrhosis, liver cancer, cholestasis. AST also elevated in MI, rhabdomyolysis, muscle injury. AST:ALT ratio >2:1 suggests alcoholic liver disease. Drug-induced hepatotoxicity: acetaminophen (#1 cause), statins, isoniazid, valproic acid \u2014 monitor LFTs. Markedly elevated (>1000): acute hepatitis, acetaminophen toxicity, ischemic hepatitis. Mild elevation (2-3\u00d7 normal): fatty liver, chronic hepatitis, medications."),

    # 18 - Bilirubin
    ("Bilirubin: Normal ranges and types?",
     "Total bilirubin: 0.1-1.2 mg/dL. Direct (conjugated): 0-0.3 mg/dL \u2014 elevated in obstructive jaundice (gallstones, pancreatic head tumor, biliary stricture). Indirect (unconjugated): 0.2-0.8 mg/dL \u2014 elevated in hemolytic conditions (sickle cell, transfusion reaction, hemolytic disease of newborn), impaired conjugation (Gilbert syndrome, neonatal jaundice). Clinical significance: jaundice visible when total bilirubin >2.5-3.0 mg/dL (skin, sclera). Assess jaundice in natural light. Neonates: pathologic if total bilirubin >12-15 mg/dL (term) or appearing within first 24 hours. Kernicterus risk with very high levels (>25-30 mg/dL). Dark urine (tea-colored) with elevated direct bilirubin; clay-colored stools with obstructive jaundice."),

    # 19 - Albumin
    ("Albumin: Normal range and clinical significance?",
     "Normal: 3.5-5.0 g/dL. Major plasma protein produced by liver \u2014 maintains oncotic pressure, transports drugs, reflects nutritional status. Decreased (<3.5): malnutrition (takes 2-3 weeks to reflect dietary changes \u2014 prealbumin is more sensitive for acute changes), liver disease (cirrhosis \u2014 can't produce albumin), nephrotic syndrome (lost in urine), burns, inflammatory states. Consequences: peripheral edema, ascites, impaired wound healing. Affects drug binding: low albumin \u2192 higher free drug levels (increased effect/toxicity) \u2014 important for phenytoin, warfarin. Critically low: <2.0 g/dL. Prealbumin (transthyretin): 15-36 mg/dL \u2014 better indicator of recent nutritional status (half-life 2-3 days vs albumin 20 days)."),

    # 20 - Troponin
    ("Troponin: Normal range and significance in acute MI?",
     "Normal: <0.04 ng/mL (conventional assay); high-sensitivity troponin: <14 ng/L (varies by assay). Troponin I and T: cardiac-specific biomarkers \u2014 most sensitive and specific for myocardial injury. Timing: rises 3-6 hours after MI onset, peaks 12-24 hours, remains elevated 7-14 days (troponin I) or 10-14 days (troponin T). Serial measurements: draw at presentation, 3-6 hrs, optionally at 6-12 hrs. Rising pattern confirms acute MI. Other causes of elevated troponin (not MI): PE, myocarditis, heart failure exacerbation, renal failure, sepsis, cardioversion. Always interpret in clinical context. High-sensitivity troponin can detect very small amounts \u2014 improves early rule-out. Critical value: any elevation above 99th percentile of normal reference."),

    # 21 - BNP
    ("BNP (B-Type Natriuretic Peptide): Normal range and use in heart failure?",
     "BNP: <100 pg/mL (normal). NT-proBNP: <300 pg/mL for rule-out of acute HF. Released from ventricles in response to volume overload and increased wall stress. BNP >100 pg/mL: suggests heart failure. BNP >400 pg/mL: high likelihood of HF. Used to: differentiate cardiac from pulmonary dyspnea, monitor HF treatment effectiveness (should decrease with effective treatment), and guide prognosis (higher BNP = worse prognosis). Falsely low in obesity. Falsely elevated in renal failure, atrial fibrillation, PE, advanced age. Track trends over time rather than single values."),

    # 22 - CK-MB
    ("CK-MB: Normal range and when is it used?",
     "Normal CK-MB: <5% of total CK (or <25 IU/L). CK-MB is the cardiac-specific fraction of creatine kinase. Rises 4-8 hours after MI, peaks 12-24 hours, returns to normal in 48-72 hours. Clinical use: largely replaced by troponin for MI diagnosis but still useful for: detecting reinfarction (returns to normal faster than troponin \u2014 a second rise indicates new event), timing of MI, and perioperative MI detection. Total CK: 30-170 U/L (male), 25-150 U/L (female). Also elevated in rhabdomyolysis (CK >5\u00d7 normal, often >10,000), muscle trauma, strenuous exercise."),

    # 23 - Thyroid
    ("TSH, T3, and T4: Normal ranges and interpretation?",
     "TSH: 0.5-4.0 mIU/L (most sensitive screening test \u2014 interpret FIRST). Free T4: 0.8-1.8 ng/dL. Free T3: 2.3-4.2 pg/mL. Hypothyroidism: TSH HIGH, T3/T4 LOW (thyroid underproducing \u2192 pituitary increases TSH). Symptoms: fatigue, weight gain, cold intolerance, constipation, bradycardia, dry skin, depression, myxedema. Treatment: levothyroxine. Hyperthyroidism: TSH LOW, T3/T4 HIGH (thyroid overproducing \u2192 pituitary suppresses TSH). Symptoms: weight loss, heat intolerance, tachycardia/afib, tremor, diarrhea, exophthalmos (Graves disease), anxiety. Treatment: methimazole (PTU in first trimester or thyroid storm), radioactive iodine, surgery. Thyroid storm: extreme hyperthyroidism \u2014 fever >104\u00b0F, tachycardia, delirium \u2014 emergency."),

    # 24 - A1C
    ("Hemoglobin A1C: Normal range and target goals?",
     "Normal: <5.7%. Pre-diabetes: 5.7-6.4%. Diabetes diagnosis: \u22656.5%. Reflects average blood glucose over past 2-3 months (lifespan of RBC). Target for most diabetics: <7.0% (ADA recommendation). Elderly/comorbid patients: may accept <8.0% (avoid hypoglycemia). Estimated average glucose (eAG): A1C 6% \u2248 126 mg/dL, 7% \u2248 154 mg/dL, 8% \u2248 183 mg/dL, 9% \u2248 212 mg/dL, 10% \u2248 240 mg/dL (formula: eAG = 28.7 \u00d7 A1C - 46.7). Conditions affecting accuracy: hemolytic anemia, chronic bleeding, transfusions, sickle cell disease \u2014 may falsely lower A1C. Iron deficiency anemia may falsely elevate A1C. Test every 3-6 months in diabetic patients."),

    # 25 - Lipid Panel
    ("Lipid panel: Normal values and target goals?",
     "Total cholesterol: <200 mg/dL (desirable), 200-239 (borderline high), \u2265240 (high). LDL ('bad' cholesterol): <100 mg/dL (optimal), <70 mg/dL (high-risk/CAD patients on statin therapy). HDL ('good' cholesterol): >40 mg/dL (male), >50 mg/dL (female) \u2014 higher is better (\u226560 is protective). Triglycerides: <150 mg/dL (normal), 150-199 (borderline), 200-499 (high), \u2265500 (very high \u2014 pancreatitis risk). Fasting: 9-12 hours for accurate triglycerides/LDL. Non-HDL cholesterol = Total - HDL (secondary target). Statins: first-line for LDL lowering \u2014 monitor LFTs, CK (rhabdomyolysis risk), teach: take at bedtime (some statins), avoid grapefruit (some statins), report muscle pain."),

    # 26 - ABG Normals
    ("ABG normal values: Complete reference?",
     "pH: 7.35-7.45. PaCO2: 35-45 mmHg (respiratory component \u2014 acid). PaO2: 80-100 mmHg (oxygenation \u2014 not acid-base). HCO3: 22-26 mEq/L (metabolic component \u2014 base). SaO2: >95%. Base excess/deficit: -2 to +2 mEq/L (negative = base deficit = metabolic acidosis; positive = base excess = metabolic alkalosis). Quick interpretation: pH and PaCO2 move in OPPOSITE directions = respiratory cause. pH and HCO3 move in SAME direction = metabolic cause. Compensation: the unaffected system moves to normalize pH. Full compensation = normal pH. The system that moved FIRST (and is more abnormal) is the primary disorder."),

    # 27 - Urinalysis
    ("Urinalysis normal values: Key components?",
     "Color: pale yellow to amber. Clarity: clear. Specific gravity: 1.005-1.030 (higher = concentrated/dehydrated, lower = dilute/overhydrated, diabetes insipidus). pH: 4.5-8.0 (average 6.0). Protein: negative (positive = kidney damage, preeclampsia, nephrotic syndrome). Glucose: negative (positive = DM with glucose >180 mg/dL \u2014 renal threshold). Ketones: negative (positive = DKA, starvation, low-carb diet). Blood: negative (positive = UTI, kidney stones, glomerulonephritis, menstruation). Nitrites: negative (positive suggests bacterial infection \u2014 gram-negative bacteria convert nitrates to nitrites). Leukocyte esterase: negative (positive = WBCs in urine, infection). WBC: 0-5/HPF. RBC: 0-3/HPF. Casts: none (RBC casts = glomerulonephritis, WBC casts = pyelonephritis, waxy casts = chronic renal failure). Bacteria: none."),

    # 28 - Critical Values (CORRECTED: Potassium >6.5 -> >6.0)
    ("Critical lab values that require IMMEDIATE provider notification?",
     "Potassium: <2.5 or >6.0 mEq/L (cardiac arrest risk). Sodium: <120 or >160 mEq/L (seizures, neurological damage). Glucose: <40 or >500 mg/dL. Calcium: <6.0 or >13.0 mg/dL. Magnesium: <1.0 or >4.7 mEq/L. Hemoglobin: <7.0 or >20 g/dL. Platelets: <50,000 or >1,000,000/mm\u00b3. WBC: <2,000 or >30,000/mm\u00b3. INR: >5.0. aPTT: >100 seconds. Troponin: any elevation above normal. pH: <7.20 or >7.60. PaCO2: <20 or >60 mmHg. PaO2: <40 mmHg. Lactate: >4.0 mmol/L. Positive blood cultures. Nursing responsibility: read back results, document time of notification, name of provider notified, and any orders received. Follow institution's critical value reporting policy \u2014 typically notify within 30-60 minutes."),

    # 29 - D-dimer
    ("D-dimer: Normal value and clinical use?",
     "Normal: <500 ng/mL (or <0.5 mcg/mL FEU). D-dimer is a fibrin degradation product \u2014 elevated when clots are being broken down. Clinical use: HIGH negative predictive value \u2014 if normal, effectively RULES OUT DVT/PE (in low-to-moderate pretest probability). If elevated: NOT diagnostic \u2014 requires further imaging (CT-PA for PE, duplex ultrasound for DVT). Also elevated in: DIC, post-surgery, trauma, pregnancy, malignancy, infection, liver disease, advanced age. Not useful for monitoring anticoagulation therapy. Best used as a rule-out test, not a rule-in test."),

    # 30 - Lactate
    ("Lactate: Normal range and significance in sepsis?",
     "Normal: 0.5-2.0 mmol/L. Elevated lactate indicates tissue hypoperfusion/anaerobic metabolism. Causes: sepsis/septic shock, cardiogenic shock, hypovolemia, severe hypoxia, liver failure (decreased clearance), medications (metformin, epinephrine), seizures, strenuous exercise. In sepsis: lactate >2 mmol/L indicates tissue hypoperfusion. Lactate >4 mmol/L: high mortality risk \u2014 triggers aggressive resuscitation (SEP-1 bundle). Sepsis bundle: measure lactate, blood cultures before antibiotics, broad-spectrum antibiotics within 1 hour, IV crystalloid 30 mL/kg for hypotension or lactate \u22654, vasopressors if hypotensive after fluids. Serial lactate measurements: target lactate clearance \u226510% over first 6 hours indicates response to treatment."),

    # 31 - Ammonia
    ("Ammonia: Normal range and clinical significance?",
     "Normal: 15-45 mcg/dL (varies by lab). Ammonia is produced from protein metabolism and cleared by the liver (converted to urea). Elevated: hepatic encephalopathy (liver cannot clear ammonia \u2192 crosses blood-brain barrier), Reye syndrome, urea cycle disorders, GI bleeding (blood = protein \u2192 ammonia in gut). Symptoms of hepatic encephalopathy: confusion, asterixis (flapping tremor), altered LOC \u2192 coma. Treatment: lactulose (osmotic laxative \u2014 promotes ammonia excretion in stool, goal: 2-3 soft stools/day), rifaximin (gut antibiotic \u2014 reduces ammonia-producing bacteria), protein restriction (mild/short-term only \u2014 moderate protein intake preferred). Specimen handling: collect on ice, send immediately to lab. Do NOT use tourniquet or have patient clench fist (falsely elevates)."),

    # 32 - Uric Acid
    ("Uric acid: Normal range and clinical significance?",
     "Normal: 3.5-7.2 mg/dL (male), 2.6-6.0 mg/dL (female). End product of purine metabolism. Elevated (hyperuricemia): gout (#1 association \u2014 crystal deposition in joints, especially great toe/first MTP), tumor lysis syndrome (massive cell destruction releases purines), renal calculi (uric acid stones), chronic kidney disease, thiazide diuretics, high-purine diet (red meat, organ meats, shellfish, beer). Treatment: acute gout \u2014 NSAIDs (indomethacin), colchicine, corticosteroids. Prophylaxis: allopurinol or febuxostat (xanthine oxidase inhibitors \u2014 decrease uric acid production). Tumor lysis syndrome prevention: rasburicase (recombinant urate oxidase), IV hydration, allopurinol. Teach: avoid high-purine foods, adequate hydration, limit alcohol."),

    # 33 - Prealbumin
    ("Prealbumin (transthyretin): Why is it preferred over albumin for nutritional status?",
     "Normal: 15-36 mg/dL. Half-life: 2-3 days (vs albumin's 20 days) \u2014 reflects recent nutritional changes more rapidly. Better indicator of acute nutritional status and response to nutritional intervention. Mild depletion: 10-15 mg/dL. Moderate: 5-10 mg/dL. Severe: <5 mg/dL. Decreased in: malnutrition, liver disease, inflammation (negative acute phase reactant \u2014 decreases with infection/inflammation, which limits its accuracy during acute illness). Use serial measurements to track nutritional improvement. Monitor in patients on TPN, post-surgical patients, critically ill patients. CRP can be measured alongside prealbumin \u2014 if CRP is elevated, low prealbumin may reflect inflammation rather than malnutrition."),

    # 34 - Adult Vital Signs
    ("Adult vital sign normal ranges?",
     "Temperature: 97.8-99.1\u00b0F (36.5-37.3\u00b0C). Oral is standard; rectal is most accurate (+1\u00b0F above oral); axillary is least accurate (-1\u00b0F below oral); tympanic approximates core. Fever: >100.4\u00b0F (38\u00b0C). Heart Rate: 60-100 bpm. Bradycardia <60, Tachycardia >100. Respiratory Rate: 12-20 breaths/min. Bradypnea <12, Tachypnea >20. Blood Pressure: <120/80 (normal). Pulse Oximetry: 95-100% (normal). <90% = respiratory failure. Orthostatic hypotension: SBP drop \u226520 mmHg or DBP drop \u226510 mmHg or HR increase \u226520 bpm within 3 min of standing \u2014 indicates hypovolemia. Always assess VS together \u2014 changes in one may explain others."),

    # 35 - Pediatric Vital Signs
    ("Pediatric vital signs: Why are normal ranges age-dependent?",
     "Children are NOT small adults \u2014 their physiology changes with growth. HR decreases with age: newborns rely on HR for cardiac output (cannot increase stroke volume well). RR decreases with age: smaller lungs require faster rate. BP increases with age: blood volume and vascular resistance increase. KEY PRINCIPLE: tachycardia is the FIRST sign of distress/shock in children. Hypotension is a LATE sign (indicates decompensated shock \u2014 25% blood loss). Weight-based calculations: fluid bolus 20 mL/kg NS, maintenance fluids by 4-2-1 rule (4 mL/kg/hr for first 10 kg + 2 mL/kg/hr for next 10 kg + 1 mL/kg/hr for each kg above 20). Always weigh in kilograms for medication dosing."),

    # 36 - ESR/CRP
    ("ESR and CRP: Normal ranges and uses?",
     "ESR (Erythrocyte Sedimentation Rate): Male <15 mm/hr (age <50) or <20 mm/hr (>50). Female <20 mm/hr (<50) or <30 mm/hr (>50). CRP (C-Reactive Protein): <1.0 mg/dL (or <10 mg/L). Both are nonspecific markers of inflammation \u2014 elevated in infection, autoimmune disease, malignancy, tissue injury. ESR: slow to rise (24-48 hrs) and slow to normalize. CRP: rises within 6-8 hrs and normalizes faster \u2014 better for monitoring acute changes. Uses: monitor disease activity (rheumatoid arthritis, SLE, IBD, temporal arteritis \u2014 ESR often >100 mm/hr in temporal arteritis), response to treatment, detect infection. hs-CRP (high sensitivity): <1.0 mg/L low CV risk, 1.0-3.0 moderate, >3.0 high \u2014 used for cardiovascular risk assessment."),

    # 37 - Iron Studies
    ("Iron studies: Normal values and patterns in iron deficiency anemia?",
     "Serum iron: 60-170 mcg/dL. TIBC (Total Iron Binding Capacity): 250-370 mcg/dL. Transferrin saturation: 20-50%. Ferritin: Male 12-300 ng/mL, Female 10-150 ng/mL. Iron deficiency anemia pattern: LOW serum iron, HIGH TIBC (body makes more transferrin trying to capture scarce iron), LOW ferritin (depleted iron stores), LOW transferrin saturation. Microcytic, hypochromic RBCs on smear. Ferritin is the best single test for iron deficiency (first to decrease). However, ferritin is also an acute phase reactant \u2014 can be falsely elevated in inflammation/infection even with true iron deficiency. Anemia of chronic disease: LOW iron, LOW TIBC, NORMAL or HIGH ferritin. Treatment: oral iron (ferrous sulfate \u2014 take on empty stomach with vitamin C for absorption, expect dark stools), IV iron (iron dextran \u2014 test dose required, anaphylaxis risk)."),

    # 38 - ABG Compensation
    ("ABG: Compensation rules and examples?",
     "Uncompensated: pH abnormal, one system abnormal, other system normal. Partially compensated: pH still abnormal, BOTH systems abnormal (compensating system moving to correct pH). Fully compensated: pH NORMAL (7.35-7.45), BOTH systems abnormal. To identify primary disorder when fully compensated: look at which side of 7.40 the pH falls \u2014 acidotic side (7.35-7.40) \u2192 primary acidosis; alkalotic side (7.40-7.45) \u2192 primary alkalosis. Example: pH 7.32, PaCO2 55, HCO3 30. pH acidotic, PaCO2 high (respiratory acidosis), HCO3 high (metabolic alkalosis \u2014 compensation). Primary: respiratory acidosis with partial metabolic compensation (pH still abnormal). Clinical: likely COPD with chronic CO2 retention."),

    # 39 - Coagulation Cascade
    ("Coagulation cascade: Extrinsic vs intrinsic pathway and lab tests?",
     "Extrinsic pathway: triggered by tissue factor (tissue damage) \u2192 factor VII \u2192 activates factor X. Monitored by PT/INR. Warfarin affects extrinsic pathway. Mnemonic: PT = ProThrombin time = Warfarin (P and W don't touch \u2014 remember by exclusion vs aPTT). Intrinsic pathway: triggered by contact activation (factor XII) \u2192 factors XI, IX, VIII \u2192 activates factor X. Monitored by aPTT. Heparin affects intrinsic pathway. Mnemonic: aPTT = heParin (both have P). Common pathway: factor X \u2192 prothrombin \u2192 thrombin \u2192 fibrinogen \u2192 fibrin clot. Both PT and aPTT affected by common pathway issues (factor X, V, prothrombin, fibrinogen). DIC affects all pathways: elevated PT, aPTT, D-dimer; decreased fibrinogen and platelets."),

    # 40 - Newborn vital signs
    ("Newborn vital signs: Normal ranges?",
     "Heart Rate: 120-160 bpm (may be 100 during sleep, up to 180 with crying). Respiratory Rate: 30-60 breaths/min. Periodic breathing is normal (pauses <20 sec); apnea = pause >20 sec or any pause with bradycardia/cyanosis. Temperature: 97.7-99.5\u00b0F (36.5-37.5\u00b0C) axillary. Blood Pressure: 60-80/40-50 mmHg (term newborn). SpO2: pre-ductal (right hand) \u226595%, post-ductal (left hand or foot) \u226595%, difference <3% (screening for critical congenital heart disease). Weight: average term 2,500-4,000g (5.5-8.8 lbs). Normal weight loss: up to 7-10% in first 3-5 days; regain birth weight by 10-14 days."),

    # 41 - Infant vital signs
    ("Infant vital signs (1-12 months): Normal ranges?",
     "Heart Rate: 100-160 bpm (decreases as infant grows). Respiratory Rate: 24-40 breaths/min. Temperature: 97.7-99.5\u00b0F (36.5-37.5\u00b0C). Blood Pressure: approximately 80-100/50-65 mmHg (increases with age). Key assessment: anterior fontanelle (soft spot) \u2014 bulging = increased ICP (meningitis, hydrocephalus), sunken = dehydration. Closes by 12-18 months. Posterior fontanelle closes by 2-3 months. Weight milestones: doubles birth weight by 5-6 months, triples by 12 months. Head circumference: most important growth parameter in first year (brain growth). Measure at every well visit."),

    # 42 - Toddler/Preschool vital signs
    ("Toddler/Preschool (1-5 years) vital signs: Normal ranges?",
     "Heart Rate: 80-130 bpm (1-3 years), 80-120 bpm (3-5 years). Respiratory Rate: 20-30 breaths/min. Blood Pressure: approximately 90-105/55-70 mmHg. Hypertension in children: >95th percentile for age/height/sex on 3+ separate occasions. Temperature: same as adult norms. Key considerations: toddlers cannot localize pain well \u2014 may present with irritability, decreased activity, poor feeding. Use age-appropriate pain scales (FLACC for preverbal). Growth: weight quadruples birth weight by 2.5 years. Height at age 2 is approximately half adult height."),

    # 43 - School-age/Adolescent vital signs
    ("School-age (6-12) and Adolescent (13-18) vital signs: Normal ranges?",
     "School-age HR: 70-110 bpm. Adolescent HR: 60-100 bpm (approaching adult). School-age RR: 18-25 breaths/min. Adolescent RR: 12-20 breaths/min (adult range). School-age BP: approximately 100-120/60-75 mmHg. Adolescent BP: approaching adult norms (<120/80). Screen for hypertension annually starting at age 3. Adolescent-specific: screen for scoliosis, eating disorders, depression, substance use. Tanner staging for pubertal development. BMI screening: >85th percentile = overweight, >95th percentile = obese."),

    # 44 - Blood glucose monitoring
    ("Blood glucose monitoring: Timing, technique, and nursing considerations?",
     "Timing: fasting (before meals), 2-hour postprandial, before bedtime, at 3 AM (Somogyi effect vs dawn phenomenon). Technique: wash hands with warm water (no alcohol \u2014 can affect reading), use side of fingertip (less painful, better blood flow), rotate puncture sites, do not squeeze excessively (dilutes with tissue fluid). Target ranges: pre-meal 80-130 mg/dL, peak postprandial <180 mg/dL (ADA). Continuous glucose monitoring (CGM): measures interstitial glucose every 5 minutes, 5-15 minute lag behind blood glucose, useful for trend identification. Time in range (TIR): goal >70% of time between 70-180 mg/dL. Somogyi effect: nocturnal hypoglycemia \u2192 rebound morning hyperglycemia (treatment: reduce evening insulin or add bedtime snack). Dawn phenomenon: early morning growth hormone/cortisol surge \u2192 hyperglycemia (treatment: adjust basal insulin timing)."),

    # 45 - Blood pressure categories
    ("Blood pressure categories and hypertension staging (adults)?",
     "Normal: <120/80 mmHg. Elevated: SBP 120-129 AND DBP <80. Stage 1 Hypertension: SBP 130-139 OR DBP 80-89. Stage 2 Hypertension: SBP \u2265140 OR DBP \u226590. Hypertensive Crisis: SBP >180 AND/OR DBP >120 \u2014 assess for target organ damage (headache, visual changes, chest pain, dyspnea, neurological deficits). Hypertensive urgency: severely elevated without organ damage \u2014 reduce BP gradually over 24-48 hours. Hypertensive emergency: with organ damage \u2014 IV medications (nitroprusside, labetalol, nicardipine), reduce MAP by no more than 25% in first hour (too rapid = stroke, MI, renal failure). Proper BP measurement: rest 5 min, empty bladder, supported arm at heart level, appropriate cuff size (bladder 80% of arm circumference)."),

    # 46 - Oxygen saturation and delivery
    ("Pulse oximetry: Normal values and factors affecting accuracy?",
     "Normal SpO2: 95-100%. Mild hypoxemia: 91-94%. Moderate hypoxemia: 86-90%. Severe hypoxemia: <85%. Factors causing FALSE readings: motion artifact, poor perfusion (shock, hypothermia, vasoconstriction), dark nail polish (especially blue, black, green \u2014 remove or use earlobe/forehead sensor), carbon monoxide poisoning (SpO2 reads falsely HIGH because CO-Hgb absorbs light similarly to O2-Hgb \u2014 get ABG with co-oximetry), methemoglobinemia (reads ~85% regardless of true saturation), anemia (SpO2 may be normal despite inadequate O2 delivery \u2014 check Hgb), ambient light interference. PaO2 vs SpO2: PaO2 80-100 mmHg = SpO2 95-100%. PaO2 60 mmHg = SpO2 ~90% (critical point on oxyhemoglobin dissociation curve \u2014 below this, saturation drops rapidly)."),

    # 47 - Temperature assessment
    ("Temperature: Routes, normal ranges, and fever management?",
     "Routes and accuracy: Rectal = most accurate core temp (contraindicated in neutropenia, rectal surgery, neonates in some facilities). Oral = standard in adults (wait 15-30 min after eating/drinking). Tympanic = reflects core temp, quick, but technique-dependent. Temporal artery = noninvasive, reasonable accuracy. Axillary = least accurate, used when other routes contraindicated. Conversions: F = (C \u00d7 9/5) + 32; C = (F - 32) \u00d7 5/9. Fever: >100.4\u00b0F (38\u00b0C). Hyperthermia vs fever: fever = hypothalamic setpoint elevated (infection, inflammation); hyperthermia = body overwhelmed/setpoint normal (heat stroke, malignant hyperthermia). Malignant hyperthermia: genetic reaction to succinylcholine/volatile anesthetics \u2014 treat with dantrolene. Hypothermia: <95\u00b0F (35\u00b0C) \u2014 mild 90-95\u00b0F, moderate 82-90\u00b0F, severe <82\u00b0F. Rewarm gradually."),

    # 48 - Pain assessment scales
    ("Pain as the 'fifth vital sign': Assessment scales and documentation?",
     "Numeric Rating Scale (NRS): 0-10, for adults and children >7 years who can self-report. Wong-Baker FACES: ages 3-7+, patient points to face matching pain level. FLACC Scale: ages 2 months to 7 years or nonverbal \u2014 Face, Legs, Activity, Cry, Consolability (0-2 each, total 0-10). CPOT (Critical Care Pain Observation Tool): for intubated/unconscious patients \u2014 facial expression, body movements, muscle tension, ventilator compliance. PAINAD: for dementia patients \u2014 breathing, vocalization, facial expression, body language, consolability. Assessment: use consistent scale, assess before and after interventions (30 min post-IV, 60 min post-PO), document location, quality, onset, duration, aggravating/alleviating factors. WHO pain ladder: Step 1 non-opioid (acetaminophen, NSAIDs), Step 2 weak opioid, Step 3 strong opioid."),

    # 49 - Intake and output
    ("Intake and Output (I&O): Normal values and monitoring?",
     "Normal adult urine output: 0.5-1.0 mL/kg/hr (approximately 30-60 mL/hr or 1,500-2,000 mL/day). Oliguria: <400 mL/day or <0.5 mL/kg/hr (may indicate AKI, dehydration, shock). Anuria: <100 mL/day (renal failure, obstruction). Polyuria: >3,000 mL/day (diabetes insipidus, DM, diuretics, psychogenic polydipsia). Intake includes: oral fluids, IV fluids, tube feeding, IV medications/flushes, blood products, irrigation fluid retained. Output includes: urine, emesis, wound drainage (chest tube, JP, Hemovac), NG suction, stool (especially diarrhea), estimated blood loss. Normal insensible loss: ~500-1,000 mL/day (lungs, skin) \u2014 increases with fever, tachypnea, burns. Pediatric urine output: infant 2 mL/kg/hr, child 1 mL/kg/hr, adolescent 0.5 mL/kg/hr. Wet diapers: minimum 6-8/day for adequate hydration in infants."),

    # 50 - Fluid and electrolyte balance
    ("Fluid balance: Dehydration vs fluid overload assessment?",
     "Dehydration signs: thirst, dry mucous membranes, decreased skin turgor (tenting), sunken eyes/fontanelle (infants), tachycardia, hypotension, orthostatic changes, oliguria, concentrated urine (high specific gravity >1.030), elevated BUN/creatinine ratio (>20:1), weight loss (1 L fluid = 1 kg = 2.2 lbs). Mild: 3-5% weight loss, Moderate: 6-9%, Severe: >10%. Fluid overload signs: edema (peripheral, periorbital, sacral in bedridden patients), weight gain, distended neck veins (JVD), crackles/rales in lungs, dyspnea, S3 heart sound, bounding pulse, elevated BP, decreased BUN/Hct (hemodilution), low urine specific gravity. Treatment: dehydration \u2014 isotonic IV fluids (0.9% NS or LR), oral rehydration. Fluid overload \u2014 fluid restriction, diuretics (furosemide), sodium restriction, elevate HOB, monitor daily weights (same time, same scale, same clothing). I&O monitoring essential for both."),
]

deck = {
    "slug": "nursing-lab-values",
    "title": "Nursing: Lab Values & Vital Signs",
    "category": "Professional",
    "description": "Essential lab values, vital signs, and critical values for nursing students. Covers electrolytes, CBC, coagulation, cardiac markers, ABGs, and age-specific vital sign ranges.",
    "meta_desc": "Free nursing lab values flashcards. 50 cards covering electrolytes, CBC, coagulation, cardiac markers, ABGs, vital signs, and critical values. Study for NCLEX online.",
    "keywords": "nursing lab values, NCLEX lab values, nursing flashcards, critical lab values, vital signs nursing, ABG interpretation, electrolyte imbalances",
    "color": {"hex": "#007AFF", "r": 0.0, "g": 0.478, "b": 1.0},
    "cards": CARDS,
}

def build_card_html(cards):
    rows = []
    for front, back in cards:
        rows.append(
            f'        <div class="card-item">'
            f'<div class="card-front">{html.escape(front)}</div>'
            f'<div class="card-back">{html.escape(back)}</div>'
            f'</div>'
        )
    return "\n".join(rows)

def build_deck_json(d):
    return json.dumps({
        "title": d["title"],
        "cards": [[f, b] for f, b in d["cards"]],
        "color": d["color"],
    }, ensure_ascii=False)

def main():
    d = deck
    card_html = build_card_html(d["cards"])
    deck_json = build_deck_json(d)
    page_title = f"{d['title']} Flashcards"
    card_count = len(d["cards"])

    page = TEMPLATE.format(
        page_title=page_title,
        meta_desc=d["meta_desc"],
        keywords=d["keywords"],
        slug=d["slug"],
        title=d["title"],
        description=d["description"],
        category=d["category"],
        card_count=card_count,
        card_html=card_html,
        deck_json=deck_json,
    )

    out_dir = os.path.join(SITE, "decks")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{d['slug']}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"[SUCCESS] Generated {out_path} ({card_count} cards)")

if __name__ == "__main__":
    main()
