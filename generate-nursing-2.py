#!/usr/bin/env python3
"""Generate nursing flashcard deck pages for Maternal/Newborn and Pediatric.
Reads card data from the task output file, applies corrections, and generates HTML."""
import json, html, re, os, ast

SITE = "/Users/stephaniedugas/Documents/stacked-site"

# ── Step 1: Extract card data from source file ──────────────────────────────

SOURCE = "/private/tmp/claude-501/-Users-stephaniedugas/c3c54a3d-841a-421a-a11e-530f03615d0b/tasks/ac8aae753b4e8e3a7.output"

with open(SOURCE, "r") as f:
    lines = f.readlines()

# Parse assistant response (line 2, index 1)
data = json.loads(lines[1])
content = data.get("message", {}).get("content", "")
if isinstance(content, list):
    content = "\n".join(
        [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
    )

# Also append line 3 if it exists (continuation)
if len(lines) > 2:
    data3 = json.loads(lines[2])
    c3 = data3.get("message", {}).get("content", "")
    if isinstance(c3, list):
        c3 = "\n".join(
            [c.get("text", "") for c in c3 if isinstance(c, dict) and c.get("type") == "text"]
        )
    content = content + "\n" + c3

# Locate deck sections
deck3_start = content.find("DECK 3")
deck4_start = content.find("DECK 4")
deck5_start = content.find("DECK 5")
if deck5_start == -1:
    deck5_start = len(content)

deck3_text = content[deck3_start:deck4_start]
deck4_text = content[deck4_start:deck5_start]


def extract_cards_from_section(text):
    """Extract card tuples from a section of text containing Python code blocks.
    Handles cases where content is split across JSON lines."""
    # Strategy: scan the ENTIRE section text for tuples, not just code blocks.
    # This handles cases where code blocks are split across JSON lines.
    cards = []

    # First try: find a complete code block and parse it
    code_match = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if code_match:
        code = code_match.group(1)
        list_match = re.search(r"=\s*(\[.*)", code, re.DOTALL)
        if list_match:
            list_str = list_match.group(1).strip()
            try:
                return ast.literal_eval(list_str)
            except SyntaxError:
                pass

    # Fallback: scan ALL text for tuples using balanced-paren extraction
    # This catches cards even when code blocks are split
    i = 0
    while i < len(text):
        # Look for pattern: ("
        if text[i] == "(" and i + 1 < len(text) and text[i + 1] == '"':
            # Find the matching closing paren using depth tracking
            depth = 1
            j = i + 1
            in_string = False
            while j < len(text) and depth > 0:
                ch = text[j]
                if in_string:
                    if ch == "\\" and j + 1 < len(text):
                        j += 1  # skip escaped char
                    elif ch == '"':
                        in_string = False
                else:
                    if ch == '"':
                        in_string = True
                    elif ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                j += 1
            if depth == 0:
                tuple_str = text[i:j]
                try:
                    card = ast.literal_eval(tuple_str)
                    if isinstance(card, tuple) and len(card) == 2:
                        cards.append(card)
                        i = j
                        continue
                except:
                    pass
        i += 1

    return cards


print("Extracting DECK 3 (Maternal/Newborn)...")
deck3_cards = extract_cards_from_section(deck3_text)
print(f"  Found {len(deck3_cards)} cards")

print("Extracting DECK 4 (Pediatric)...")
deck4_cards = extract_cards_from_section(deck4_text)
print(f"  Found {len(deck4_cards)} cards from primary extraction")

# The source file has content split across JSON lines, causing some cards to be
# truncated mid-string. Add missing cards that couldn't be parsed from the split.
# These were verified from the original source content (line 3 of the output file).
deck4_known_fronts = {card[0] for card in deck4_cards}

DECK4_SUPPLEMENTAL = [
    ("Congenital heart defects: Cyanotic vs acyanotic — key differences and examples?",
     "Acyanotic (left-to-right shunt — oxygenated blood recirculates through lungs): VSD (most common CHD), ASD, PDA, coarctation of aorta. Symptoms: HF signs, frequent respiratory infections, failure to thrive, murmur. Cyanotic (right-to-left shunt — deoxygenated blood enters systemic circulation): Tetralogy of Fallot (most common cyanotic — VSD, overriding aorta, pulmonary stenosis, RV hypertrophy), Transposition of Great Arteries (TGA), Truncus Arteriosus, Tricuspid Atresia, Total Anomalous Pulmonary Venous Return. Symptoms: cyanosis (especially with crying/feeding), clubbing (chronic), tet spells (TOF — knee-chest position), polycythemia. Nursing: monitor SpO2, strict I&O, calorie-dense feedings (small frequent), cluster care to minimize O2 demand, pre/post-op cardiac surgery care, family education."),

    ("Coarctation of the aorta: Assessment, diagnosis, and nursing care?",
     "Narrowing of the aorta — usually near the ductus arteriosus (juxtaductal). Assessment: hypertension in upper extremities with hypotension/weak pulses in lower extremities (BP difference >20 mmHg between upper and lower extremities is classic), bounding radial pulses with weak/absent femoral pulses, cool lower extremities, epistaxis, headaches, dizziness, late signs of HF in neonates if severe. Often associated with bicuspid aortic valve, Turner syndrome. Diagnosis: 4-extremity BP (arms vs legs), echo, CXR (rib notching in older children), CT/MRI. Treatment: surgical repair or balloon angioplasty/stenting. Post-op: monitor for rebound hypertension, assess femoral pulses and lower extremity perfusion, monitor for abdominal pain (mesenteric arteritis), BP in all 4 extremities. Long-term: monitor for re-coarctation, lifelong cardiology follow-up."),

    ("Family-centered care principles in pediatric nursing?",
     "Core principles: family is the constant in child's life, respect family diversity and culture, share honest and complete information, encourage family participation in care and decision-making, collaborate with families at all levels. Practical applications: open visitation, parental presence during procedures (offer — don't force), rooming-in, encourage parental participation in daily care (bathing, feeding), provide education at appropriate level, include family in care planning, sibling visitation, play therapy/child life specialist involvement. Parental coping: assess family's coping mechanisms, provide emotional support, connect with resources (social work, support groups, financial assistance). Atraumatic care: minimize physical and psychological distress — use EMLA cream before procedures, allow choices, therapeutic play, honest preparation."),

    ("Epiglottitis emergency management: Step-by-step nursing priorities?",
     "1. Do NOT examine throat, do NOT lay child supine, do NOT take oral temperature, do NOT attempt blood draws or IVs initially — any agitation can cause complete airway obstruction. 2. Allow child to remain in position of comfort (usually sitting upright, leaning forward, tripod). 3. Keep parent at bedside (reduce anxiety). 4. Have emergency airway equipment at bedside (tracheostomy tray, intubation supplies). 5. Transport to OR for controlled intubation by anesthesia/ENT. 6. After airway secured: IV access, blood cultures, IV antibiotics (ceftriaxone or ampicillin-sulbactam), IV dexamethasone. 7. Contacts: prophylactic rifampin for household contacts if H. influenzae type B confirmed."),

    ("Kawasaki disease: Assessment, diagnosis, and treatment?",
     "Acute vasculitis — leading cause of acquired heart disease in children in developed countries. Peak age: 6 months-5 years, more common in Asian descent. Diagnosis (5 of 6 criteria or 4 + coronary abnormalities): Fever >=5 days PLUS >=4 of: bilateral conjunctival injection (non-purulent), oral changes (strawberry tongue, red/cracked lips), cervical lymphadenopathy (>=1.5 cm, usually unilateral), polymorphous rash, extremity changes (erythema, edema then peeling of fingers/toes in subacute phase). Most serious complication: coronary artery aneurysm (echocardiogram at diagnosis, 2 weeks, 6-8 weeks). Treatment: IVIG (2 g/kg single dose within 10 days of onset) + high-dose aspirin (80-100 mg/kg/day in 4 doses during febrile phase then 3-5 mg/kg/day for 6-8 weeks — one of few times aspirin used in children). Monitor cardiac status, avoid live vaccines for 11 months after IVIG."),

    ("Cleft lip and cleft palate: Nursing care pre- and post-operatively?",
     "Cleft lip repair: usually at ~3 months (Rule of 10s: 10 weeks, 10 lbs, Hgb 10). Cleft palate repair: usually 9-12 months (before speech development). Pre-op: special feeding techniques — use squeeze bottles (Haberman, Pigeon), upright position, burp frequently, no standard nipple. Breastfeeding may be possible with cleft lip. Post-op cleft lip: elbow restraints (no hands to face), position on back or side (NOT on abdomen), clean suture line gently after feedings with water, avoid pacifiers, protect incision (Logan bow/steri-strips), pain management. Post-op cleft palate: avoid hard objects in mouth (no straws, spoons, pacifiers, tongue depressors), elbow restraints, feed with cup or side of spoon, soft diet, monitor for bleeding from palate. Long-term: speech therapy, dental care, ear infections (eustachian tube dysfunction), emotional support."),

    ("Nephrotic syndrome: Pathophysiology, assessment, and nursing care?",
     "Massive proteinuria leads to hypoalbuminemia leads to decreased oncotic pressure leads to generalized edema (anasarca). Most common type in children: minimal change disease. Peak age: 2-6 years. Assessment: periorbital edema (first sign, especially AM), ascites, scrotal/labial edema, weight gain, decreased urine output, foamy/frothy urine, fatigue, pallor. Labs: proteinuria (3-4+, urine protein/creatinine ratio >2), hypoalbuminemia (<2.5 g/dL), hyperlipidemia, elevated hematocrit (hemoconcentration). Treatment: corticosteroids (prednisone — first-line, most respond), cyclophosphamide for steroid-resistant, albumin infusion for severe edema (followed by diuretic), sodium restriction, no fluid restriction unless severe hyponatremia. Nursing: daily weights, I&O, abdominal girth, monitor for infection (loss of immunoglobulins), skin care (edematous skin breaks down), no live vaccines during immunosuppression, urine dipstick monitoring at home."),

    ("Lead poisoning in children: Screening, assessment, and treatment?",
     "Sources: paint in pre-1978 housing (#1 source), contaminated soil, water from lead pipes, imported toys/pottery, folk remedies. Screening: blood lead level (BLL) at 1 and 2 years (high-risk areas). CDC reference value: >=3.5 mcg/dL (action level — previously 5). Assessment: often asymptomatic at low levels. Moderate levels: abdominal pain, constipation, irritability, learning difficulties, developmental delays. Severe (>70 mcg/dL): encephalopathy (seizures, coma, vomiting, ataxia) — medical emergency. Diagnosis: venous blood lead level (capillary screens must be confirmed). Treatment: remove source (environmental remediation). BLL 3.5-44: education, follow-up testing, nutritional counseling (adequate iron, calcium, vitamin C reduce absorption). BLL 45-69: chelation therapy with succimer (DMSA) oral. BLL >=70: IV chelation (CaNa2EDTA +/- dimercaprol/BAL), hospitalize. Nursing: assess home environment, nutrition, developmental screening."),

    ("Wilms tumor (nephroblastoma): Key nursing considerations?",
     "Most common renal tumor in children. Peak age: 2-5 years. Assessment: painless abdominal mass (usually found incidentally by parent during bathing), abdominal swelling, hypertension (renin-mediated), hematuria (late), fever, malaise. CRITICAL NURSING ALERT: DO NOT PALPATE ABDOMEN — can cause rupture and tumor seeding. Place sign above bed: DO NOT PALPATE ABDOMEN. Diagnosis: abdominal ultrasound/CT. Treatment: surgical nephrectomy (followed by chemotherapy +/- radiation depending on stage). Nursing: handle gently, avoid abdominal pressure, pre-op assessment of remaining kidney function, post-op: monitor BP, I&O (remaining kidney function), assess for intestinal obstruction, protect from infection (chemotherapy). Prognosis: excellent with treatment (~90% survival for favorable histology). Monitor remaining kidney lifelong."),

    ("Cerebral palsy: Types, assessment, and nursing management?",
     "Non-progressive motor disorder from brain damage before, during, or shortly after birth. Risk factors: prematurity (#1), low birth weight, birth asphyxia, infections, kernicterus. Types: Spastic (most common, ~70-80%): increased muscle tone, hyperreflexia, scissoring gait. Dyskinetic/athetoid: involuntary writhing movements, fluctuating tone. Ataxic: poor balance, uncoordinated movements. Mixed: combination. Assessment: developmental delays (not meeting motor milestones), persistent primitive reflexes, abnormal muscle tone, feeding difficulties, intellectual disability (varies — may have normal intelligence). Nursing: multidisciplinary team (PT, OT, speech, ortho), prevent contractures (ROM exercises, bracing, positioning), nutritional support (may need G-tube), assistive devices, safety, seizure management (common comorbidity), skin integrity, family support, promote maximum independence. Medications: baclofen (spasticity), botulinum toxin (focal spasticity), anticonvulsants."),

    ("Appendicitis in children: Assessment and nursing priorities?",
     "Most common surgical emergency in children. Peak age: 10-12 years. Assessment: periumbilical pain that localizes to RLQ (McBurney's point) within 12-24 hrs, anorexia, nausea, low-grade fever, rebound tenderness, guarding, positive psoas sign, positive obturator sign. Rovsing sign: pain in RLQ with palpation of LLQ. Younger children: more difficult to diagnose, higher perforation rate (difficulty verbalizing symptoms). Labs: elevated WBC (>10,000), left shift. Diagnosis: ultrasound (first-line in peds), CT if inconclusive. Nursing priorities: NPO, IV fluids, pain management (do NOT withhold analgesics — does not mask peritoneal signs per evidence), monitor for perforation signs (sudden relief of pain then diffuse pain, high fever, rigid abdomen, absent bowel sounds). Post-appendectomy: advance diet when bowel sounds return, ambulate early, wound care, antibiotics if perforated."),
]

# Add supplemental cards that weren't already extracted
added = 0
for front, back in DECK4_SUPPLEMENTAL:
    # Check if this card (or similar) was already extracted
    already_present = False
    for existing_front, _ in deck4_cards:
        # Match on first 40 chars of front to handle minor differences
        if front[:40].lower() in existing_front.lower() or existing_front[:40].lower() in front.lower():
            already_present = True
            break
    if not already_present:
        deck4_cards.append((front, back))
        added += 1

print(f"  Added {added} supplemental cards (total now: {len(deck4_cards)})")

if len(deck3_cards) == 0 or len(deck4_cards) == 0:
    print("ERROR: Failed to extract cards. Check source file.")
    exit(1)


# ── Step 2: Apply corrections ───────────────────────────────────────────────

def fix_card(cards, front_substring, new_back=None, back_find=None, back_replace=None):
    """Fix a card by matching front substring. Either replace whole back or find/replace in back."""
    for i, (front, back) in enumerate(cards):
        if front_substring.lower() in front.lower():
            if new_back is not None:
                cards[i] = (front, new_back)
            elif back_find is not None and back_replace is not None:
                cards[i] = (front, back.replace(back_find, back_replace))
            return True
    return False


# ── Maternal/Newborn corrections ──

# Cervical dilation: remove "dilates ~1 cm/hr" or update
for i, (front, back) in enumerate(deck3_cards):
    if "1 cm/hr" in back or "1cm/hr" in back:
        new_back = re.sub(
            r"[^.;]*dilates?\s*~?\s*1\s*cm/hr[^.;]*[.;]?\s*",
            "Current ACOG evidence suggests slower progress is normal; the 1 cm/hr expectation is outdated. ",
            back,
        )
        deck3_cards[i] = (front, new_back.strip())
        print(f"  Fixed cervical dilation in card: {front[:60]}")

# Homan's sign
for i, (front, back) in enumerate(deck3_cards):
    if "homan" in front.lower() or "homan" in back.lower():
        new_back = back
        # Replace any mention of Homan's sign assessment
        if "homan" in back.lower():
            new_back = re.sub(
                r"[^.;]*[Hh]oman.?s\s+sign[^.;]*[.;]?\s*",
                "Homan's sign is no longer recommended for DVT assessment (poor sensitivity/specificity, risk of clot dislodgement). Assess for calf pain, warmth, swelling, redness instead. ",
                new_back,
            )
        deck3_cards[i] = (front, new_back.strip())
        print(f"  Fixed Homan's sign in card: {front[:60]}")

# GBS screening: 35-37 weeks -> 36 0/7 to 37 6/7 weeks
for i, (front, back) in enumerate(deck3_cards):
    if "gbs" in front.lower() or "group b strep" in front.lower() or "gbs" in back.lower():
        new_back = back.replace("35-37 weeks", "36 0/7 to 37 6/7 weeks (updated CDC/ACOG 2020)")
        new_back = new_back.replace("35–37 weeks", "36 0/7 to 37 6/7 weeks (updated CDC/ACOG 2020)")
        if new_back != back:
            deck3_cards[i] = (front, new_back)
            print(f"  Fixed GBS screening in card: {front[:60]}")

# Bishop score
for i, (front, back) in enumerate(deck3_cards):
    if "bishop" in front.lower():
        # Fix scoring description
        new_back = re.sub(
            r"[Ss]cored?\s*0[\-–]3[^.;]*",
            "Dilation, effacement, station scored 0-3; consistency and position scored 0-2; max total 13",
            back,
        )
        if new_back == back:
            # Try another pattern - just append correction if not found
            if "max" not in back.lower() or "13" not in back:
                new_back = back.rstrip(". ") + ". Dilation, effacement, station scored 0-3; consistency and position scored 0-2; max total 13."
        deck3_cards[i] = (front, new_back)
        print(f"  Fixed Bishop score in card: {front[:60]}")

# Babinski reflex: disappears ~2 years -> disappears by 12-24 months
for i, (front, back) in enumerate(deck3_cards):
    if "babinski" in front.lower() or "babinski" in back.lower():
        new_back = re.sub(
            r"disappears?\s*~?\s*2\s*years?",
            "disappears by 12-24 months",
            back,
            flags=re.IGNORECASE,
        )
        new_back = re.sub(
            r"disappears?\s*~?\s*24\s*months?",
            "disappears by 12-24 months",
            new_back,
            flags=re.IGNORECASE,
        )
        if new_back != back:
            deck3_cards[i] = (front, new_back)
            print(f"  Fixed Babinski reflex in card: {front[:60]}")

# Postpartum hemorrhage: keep >1000 mL (verify it's there, no change needed)
for i, (front, back) in enumerate(deck3_cards):
    if "postpartum hemorrhage" in front.lower() or "postpartum hemorrhage" in back.lower():
        if "1000" in back or "1,000" in back:
            print(f"  Verified PPH >1000 mL is correct in card: {front[:60]}")
        elif "500" in back:
            new_back = back.replace(">500 mL", ">1000 mL (current ACOG definition)")
            new_back = new_back.replace(">500mL", ">1000 mL (current ACOG definition)")
            deck3_cards[i] = (front, new_back)
            print(f"  Fixed PPH threshold to >1000 mL in card: {front[:60]}")


# ── Pediatric corrections ──

# DKA glucose: >300 -> >250 mg/dL
for i, (front, back) in enumerate(deck4_cards):
    if ">300" in back:
        new_back = back.replace(">300", ">250 mg/dL")
        deck4_cards[i] = (front, new_back)
        print(f"  Fixed DKA glucose in card: {front[:60]}")
    if ">300" in front:
        new_front = front.replace(">300", ">250 mg/dL")
        deck4_cards[i] = (new_front, deck4_cards[i][1])
        print(f"  Fixed DKA glucose in card front: {new_front[:60]}")

# Pediatric A1C: <7.5% -> <7.0%
for i, (front, back) in enumerate(deck4_cards):
    if "<7.5%" in back or "< 7.5%" in back:
        new_back = back.replace("<7.5%", "<7.0% (updated ADA 2022)")
        new_back = new_back.replace("< 7.5%", "<7.0% (updated ADA 2022)")
        deck4_cards[i] = (front, new_back)
        print(f"  Fixed A1C in card: {front[:60]}")
    if "<7.5%" in front or "< 7.5%" in front:
        new_front = front.replace("<7.5%", "<7.0% (updated ADA 2022)")
        new_front = new_front.replace("< 7.5%", "<7.0% (updated ADA 2022)")
        deck4_cards[i] = (new_front, deck4_cards[i][1])
        print(f"  Fixed A1C in card front: {new_front[:60]}")

# Cool mist for croup: add note about evidence
for i, (front, back) in enumerate(deck4_cards):
    if "croup" in front.lower() or "croup" in back.lower():
        if "mist" in back.lower() or "cool" in back.lower() or "humidif" in back.lower():
            if "evidence does not support" not in back.lower():
                new_back = back.rstrip(". ") + ". Note: Evidence does not support mist therapy; current practice favors dexamethasone and nebulized epinephrine."
                deck4_cards[i] = (front, new_back)
                print(f"  Fixed croup mist therapy in card: {front[:60]}")

# Separation anxiety peak: 8-12 months -> 10-18 months
for i, (front, back) in enumerate(deck4_cards):
    if "separation" in front.lower() or "separation" in back.lower():
        new_back = back.replace("8-12 months", "10-18 months")
        new_back = new_back.replace("8–12 months", "10-18 months")
        if new_back != back:
            deck4_cards[i] = (front, new_back)
            print(f"  Fixed separation anxiety in card: {front[:60]}")


# ── Step 3: Generate HTML using template ─────────────────────────────────────

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


# ── Step 4: Deck definitions ────────────────────────────────────────────────

# Convert hex to RGB floats
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return round(r, 3), round(g, 3), round(b, 3)


DECKS = [
    {
        "slug": "nursing-maternal-newborn",
        "title": "Nursing: Maternal/Newborn",
        "category": "Professional",
        "description": "Essential maternal and newborn nursing concepts covering prenatal care, labor and delivery, fetal monitoring, postpartum care, and newborn assessment.",
        "meta_desc": "Free Maternal/Newborn nursing flashcards. Prenatal care, labor stages, fetal monitoring, postpartum assessment, and newborn care. Study for NCLEX online.",
        "keywords": "maternal newborn nursing flashcards, OB nursing study cards, NCLEX maternal newborn, labor and delivery flashcards, postpartum nursing",
        "color": {"hex": "#AF52DE", "r": hex_to_rgb("#AF52DE")[0], "g": hex_to_rgb("#AF52DE")[1], "b": hex_to_rgb("#AF52DE")[2]},
        "cards": deck3_cards,
    },
    {
        "slug": "nursing-pediatric",
        "title": "Nursing: Pediatric",
        "category": "Professional",
        "description": "Key pediatric nursing concepts covering growth and development, childhood illnesses, medication calculations, and family-centered care.",
        "meta_desc": "Free Pediatric nursing flashcards. Growth milestones, childhood diseases, medication calculations, and pediatric assessment. Study for NCLEX online.",
        "keywords": "pediatric nursing flashcards, peds nursing study cards, NCLEX pediatric, childhood illness flashcards, pediatric assessment",
        "color": {"hex": "#5AC8FA", "r": hex_to_rgb("#5AC8FA")[0], "g": hex_to_rgb("#5AC8FA")[1], "b": hex_to_rgb("#5AC8FA")[2]},
        "cards": deck4_cards,
    },
]


# ── Step 5: Generate HTML files ──────────────────────────────────────────────

os.makedirs(os.path.join(SITE, "decks"), exist_ok=True)

for deck in DECKS:
    card_html_lines = []
    for front, back in deck["cards"]:
        f = html.escape(front)
        b = html.escape(back)
        card_html_lines.append(
            f'        <div class="card-item"><div class="card-front">{f}</div><div class="card-back">{b}</div></div>'
        )

    card_html = "\n".join(card_html_lines)

    deck_json = json.dumps(
        {
            "title": deck["title"],
            "cards": list(deck["cards"]),
            "color": {
                "red": deck["color"]["r"],
                "green": deck["color"]["g"],
                "blue": deck["color"]["b"],
            },
        }
    )

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

print(f"\nGenerated {len(DECKS)} nursing deck pages")
