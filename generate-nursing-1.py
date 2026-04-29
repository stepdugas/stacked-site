#!/usr/bin/env python3
"""Generate nursing flashcard deck pages: Pharmacology and Cardiac/Respiratory."""
import json, html, os

SITE = "/Users/stephaniedugas/Documents/stacked-site"

DECKS = [
  {
    "slug": "nursing-pharmacology",
    "title": "Nursing Pharmacology",
    "category": "Professional",
    "description": "Essential pharmacology flashcards for nursing students covering major drug classes, mechanisms, side effects, nursing considerations, and antidotes.",
    "meta_desc": "Free nursing pharmacology flashcards. 60 cards covering cardiac drugs, anticoagulants, antibiotics, pain management, psych meds, insulin, and high-alert medications.",
    "keywords": "nursing pharmacology flashcards, NCLEX pharmacology, nursing drug cards, medication flashcards, nursing student study cards",
    "color": {"hex": "#30D158", "r": 0.188, "g": 0.820, "b": 0.345},
    "cards": [
        # Cardiac - Digoxin (CORRECTED: HR <100 infant, HR <70 older child)
        ("Digoxin (Lanoxin): Mechanism and therapeutic level?",
         "Cardiac glycoside — increases cardiac contractility (positive inotrope), decreases heart rate (negative chronotrope). Therapeutic level: 0.5–2.0 ng/mL. Check apical pulse x1 min before giving; hold if HR <60 (adult), HR <100 (infant), or HR <70 (older child). Antidote: Digibind (digoxin immune fab)."),

        ("Digoxin toxicity: Signs and risk factors?",
         "Signs: N/V, anorexia, visual disturbances (yellow-green halos, blurred vision), bradycardia, dysrhythmias. Risk factors: hypokalemia (K+ <3.5), hypomagnesemia, hypercalcemia, renal impairment. Monitor potassium closely — low K+ increases dig toxicity."),

        # Cardiac - Beta-Blockers
        ("Beta-blockers (metoprolol, atenolol, propranolol): Key nursing considerations?",
         "End in '-olol.' Decrease HR, BP, and myocardial oxygen demand. Hold if HR <60 or SBP <90. Do NOT stop abruptly — taper to avoid rebound hypertension/tachycardia. Mask hypoglycemia symptoms in diabetics. Contraindicated in asthma (propranolol — nonselective), 2nd/3rd degree heart block. Monitor for fatigue, depression, erectile dysfunction."),

        # Cardiac - ACE Inhibitors
        ("ACE inhibitors (lisinopril, enalapril, ramipril): Mechanism, side effects, and key teaching?",
         "End in '-pril.' Block conversion of angiotensin I to II — decrease BP, reduce preload/afterload. Side effects: persistent dry cough (switch to ARB if intolerable), hyperkalemia, angioedema (rare but emergent). Contraindicated in pregnancy (teratogenic). Monitor K+ and renal function (BUN/creatinine). First-dose hypotension — give at bedtime."),

        # Cardiac - ARBs
        ("ARBs (losartan, valsartan): How do they differ from ACE inhibitors?",
         "End in '-sartan.' Block angiotensin II receptors directly. Similar benefits to ACE inhibitors but do NOT cause dry cough (no bradykinin accumulation). Still contraindicated in pregnancy. Still monitor for hyperkalemia and renal function. Often used as alternative when ACE inhibitor cough is intolerable."),

        # Cardiac - Calcium Channel Blockers
        ("Calcium channel blockers: Dihydropyridines vs non-dihydropyridines?",
         "Dihydropyridines (amlodipine, nifedipine): end in '-dipine,' primarily vasodilate, reduce BP. Reflex tachycardia possible. Non-dihydropyridines (verapamil, diltiazem): reduce HR AND BP, used for rate control in afib. Both: monitor for hypotension, peripheral edema, constipation (especially verapamil). Avoid grapefruit juice (increases drug levels)."),

        # Cardiac - Nitrates
        ("Nitroglycerin: Administration, dosing, and nursing considerations?",
         "Vasodilator — primarily venous dilation, decreases preload. Sublingual: 1 tab q5min x3 doses max; call 911 if no relief after first dose (AHA guideline). Causes headache (expected), hypotension, reflex tachycardia. Remove patch at night (10-12 hr nitrate-free interval) to prevent tolerance. Store SL tabs in dark glass container; replace q6 months. Do NOT give with PDE5 inhibitors (sildenafil/Viagra) — severe hypotension."),

        # Cardiac - Antiarrhythmics
        ("Amiodarone: Key toxicities and monitoring?",
         "Class III antiarrhythmic — used for life-threatening ventricular arrhythmias and afib. Toxicities affect multiple organs: pulmonary fibrosis (baseline and annual CXR + PFTs), thyroid dysfunction (hyper or hypo — contains iodine), hepatotoxicity (monitor LFTs), corneal microdeposits (eye exams), photosensitivity (sunscreen + protective clothing). Very long half-life (40-55 days). IV: monitor for hypotension, use inline filter."),

        ("Adenosine: Use and administration?",
         "First-line for SVT (supraventricular tachycardia). Give rapid IV push (6 mg, then 12 mg if needed) followed by rapid NS flush — use port closest to heart. Causes brief asystole (3-6 sec) — warn patient they may feel chest tightness/flushing. Ultra-short half-life (<10 sec). Have crash cart at bedside. Contraindicated in 2nd/3rd degree heart block."),

        # Anticoagulants - Heparin
        ("Heparin (unfractionated): Monitoring, therapeutic range, and antidote?",
         "IV or SubQ anticoagulant. Monitor aPTT — therapeutic range: 1.5–2.5x control (typically 46–70 sec). IV requires continuous infusion pump. Never give IM. Antidote: protamine sulfate (1 mg per 100 units heparin). Risk of HIT (heparin-induced thrombocytopenia) — monitor platelet count. No need to adjust for renal impairment."),

        # Anticoagulants - Enoxaparin
        ("Enoxaparin (Lovenox): Administration and monitoring?",
         "Low-molecular-weight heparin (LMWH). SubQ only — administer in abdomen, do NOT aspirate or rub. Generally does not require routine lab monitoring. If monitored: anti-Xa level (0.5–1.0 IU/mL). Partial antidote: protamine sulfate (60% reversal). Adjust dose in renal impairment (CrCl <30: reduce dose). Longer half-life than UFH — given q12h or daily."),

        # Anticoagulants - Warfarin
        ("Warfarin (Coumadin): Monitoring, interactions, and antidote?",
         "Oral anticoagulant — inhibits vitamin K-dependent clotting factors (II, VII, IX, X). Monitor PT/INR — therapeutic INR: 2.0–3.0 (mechanical valve: 2.5–3.5). Takes 3-5 days for full effect (overlap with heparin). Antidote: vitamin K (phytonadione) for non-urgent; fresh frozen plasma or PCC for bleeding. Highly interacting: consistent vitamin K intake, avoid cranberry, many drug interactions. Teratogenic — contraindicated in pregnancy."),

        # Anticoagulants - DOACs
        ("DOACs (rivaroxaban, apixaban, dabigatran): Advantages and reversal agents?",
         "Direct oral anticoagulants. Rivaroxaban (Xarelto) and apixaban (Eliquis): factor Xa inhibitors. Dabigatran (Pradaxa): direct thrombin inhibitor. Advantages: no routine INR monitoring, fewer food interactions, predictable pharmacokinetics. Reversal: dabigatran → idarucizumab (Praxbind); rivaroxaban/apixaban → andexanet alfa (Andexxa). Renal dose adjustment needed, especially dabigatran. Take rivaroxaban with food."),

        # Antibiotics - Penicillins
        ("Penicillins (amoxicillin, ampicillin): Key nursing considerations?",
         "Beta-lactam antibiotics — inhibit cell wall synthesis. Ask about allergy before giving (cross-reactivity with cephalosporins ~1-2%). Amoxicillin: most common outpatient abx. Take on empty or full stomach. Watch for rash — maculopapular rash with EBV (mono) is NOT true allergy. Anaphylaxis risk: have epinephrine available. Complete full course. Can decrease oral contraceptive effectiveness."),

        # Antibiotics - Cephalosporins
        ("Cephalosporins: Generations and cross-allergy with penicillin?",
         "Beta-lactams — generations 1-5. 1st gen (cefazolin): gram+ skin/surgical prophylaxis. 2nd gen (cefuroxime): broader. 3rd gen (ceftriaxone): meningitis, gonorrhea. 4th gen (cefepime): pseudomonas. 5th gen (ceftaroline): MRSA. Cross-allergy with PCN: ~1-2% (low but ask). Ceftriaxone: do NOT mix with calcium-containing solutions in neonates (fatal precipitate). Disulfiram-like reaction with alcohol (some cephalosporins)."),

        # Antibiotics - Fluoroquinolones
        ("Fluoroquinolones (ciprofloxacin, levofloxacin): Black box warnings?",
         "End in '-floxacin.' FDA black box warnings: tendon rupture/tendinitis (especially Achilles — risk increased with corticosteroids and age >60), peripheral neuropathy, CNS effects (seizures, confusion), aortic aneurysm/dissection. Avoid in children <18 (cartilage damage). Separate from antacids/calcium/iron by 2 hours. Increases QT interval. Photosensitivity. Reserve for serious infections without alternatives."),

        # Antibiotics - Aminoglycosides
        ("Aminoglycosides (gentamicin, tobramycin): Toxicities and monitoring?",
         "End in '-mycin' (amino type). Bactericidal — gram-negative coverage. Two major toxicities: ototoxicity (hearing loss, tinnitus, vertigo — irreversible) and nephrotoxicity (monitor BUN/creatinine). Monitor peak and trough levels: gentamicin trough <2 mcg/mL, peak 5-10 mcg/mL (conventional dosing). Draw trough 30 min before dose, peak 30 min after infusion. Monitor I&O. Avoid concurrent nephrotoxic/ototoxic drugs."),

        # Antibiotics - Vancomycin (CORRECTED: added AUC/MIC guideline note)
        ("Vancomycin: Monitoring, infusion considerations, and adverse effects?",
         "Glycopeptide — used for MRSA, C. diff (oral only for C. diff). Updated 2020 guidelines recommend AUC/MIC-guided dosing (AUC 400-600) over traditional trough monitoring for serious MRSA infections. Traditional trough: 15–20 mcg/mL (drawn 30 min before 4th dose). Infuse over at least 60 min — rapid infusion causes Red Man Syndrome (flushing, hypotension — histamine release, not true allergy; slow rate and premedicate with diphenhydramine). Nephrotoxic and ototoxic. Monitor BUN/creatinine and hearing."),

        # Pain - Opioids
        ("Morphine: Nursing considerations and adverse effects?",
         "Opioid agonist — first-line for severe pain (MI, cancer). Adverse effects: respiratory depression (most dangerous — hold if RR <12), constipation (always order bowel regimen), sedation, urinary retention, hypotension, N/V, pruritus. Causes histamine release — can cause bronchospasm (avoid in asthma; use fentanyl or hydromorphone instead). Antidote: naloxone (Narcan). Assess pain using appropriate scale before and after administration."),

        ("Opioid equianalgesic dosing: Key conversions?",
         "Morphine 10 mg IV = morphine 30 mg PO = hydromorphone 1.5 mg IV = fentanyl 100 mcg IV. When converting between opioids, reduce dose by 25-50% for incomplete cross-tolerance. Fentanyl patch: 25 mcg/hr ≈ 60-90 mg oral morphine/day. Onset: fentanyl patch 12-24 hrs (not for acute pain). Always assess respiratory status with dose changes."),

        # Pain - NSAIDs
        ("NSAIDs (ibuprofen, naproxen, ketorolac): Risks and contraindications?",
         "Inhibit COX-1 and COX-2 — anti-inflammatory, analgesic, antipyretic. Risks: GI bleeding/ulcers (take with food, consider PPI), renal impairment (monitor BUN/Cr, maintain hydration), increased bleeding risk (inhibit platelet aggregation), cardiovascular events (especially with prolonged use). Ketorolac: max 5 days total. Contraindicated in 3rd trimester pregnancy (premature ductus arteriosus closure). Avoid in renal failure, active GI bleed. Ceiling effect for pain relief."),

        # Pain - Acetaminophen
        ("Acetaminophen toxicity: Max dose, signs, and treatment?",
         "Max dose: 4 g/day in healthy adults (2 g/day in liver disease or heavy alcohol use). Leading cause of acute liver failure. Toxicity signs: N/V in first 24 hrs → RUQ pain, elevated LFTs, jaundice at 24-72 hrs → hepatic failure at 72-96 hrs. Antidote: N-acetylcysteine (NAC) — most effective within 8 hours of ingestion. Monitor hepatic panel. Watch for hidden acetaminophen in combination products (Percocet, Vicodin, NyQuil)."),

        # Pain - Naloxone
        ("Naloxone (Narcan): Administration and key considerations?",
         "Opioid antagonist — reverses respiratory depression, sedation, and analgesia. IV/IM/SubQ/intranasal. Onset: IV 1-2 min, IM 2-5 min. Duration: 30-90 min (shorter than most opioids — monitor for re-sedation and repeat dosing). Titrate to respiratory rate, not consciousness (to avoid acute withdrawal and severe pain). May precipitate acute withdrawal: agitation, tachycardia, N/V, diaphoresis. Intranasal: 4 mg in one nostril (community use)."),

        # Psych - SSRIs
        ("SSRIs (fluoxetine, sertraline, escitalopram): Onset, side effects, and safety?",
         "First-line for depression and anxiety. Therapeutic effect takes 4-6 weeks. Side effects: sexual dysfunction, weight gain, GI upset, insomnia or drowsiness, headache. Serotonin syndrome risk if combined with MAOIs, tramadol, triptans (symptoms: hyperthermia, agitation, clonus, diaphoresis — treat with cyproheptadine). Black box warning: increased suicidality in children/adolescents/young adults (age <25) — monitor closely first 1-2 months. Do NOT stop abruptly — taper."),

        # Psych - Benzodiazepines
        ("Benzodiazepines (lorazepam, diazepam, midazolam): Safety and antidote?",
         "End in '-pam' or '-lam.' Enhance GABA — anxiolytic, sedative, anticonvulsant, muscle relaxant. Antidote: flumazenil (use cautiously — may precipitate seizures in chronic benzo users). CNS depression — do NOT combine with opioids or alcohol (respiratory depression risk). Lorazepam preferred in liver disease (no active metabolites — 'LOT' = Lorazepam, Oxazepam, Temazepam). Taper slowly — withdrawal can be fatal (seizures). Fall risk in elderly. Short-term use preferred."),

        # Psych - Lithium
        ("Lithium: Therapeutic level, toxicity, and monitoring?",
         "Mood stabilizer for bipolar disorder. Narrow therapeutic index: 0.6–1.2 mEq/L. Draw trough level 12 hours after last dose. Toxicity signs: >1.5 mEq/L — N/V, diarrhea, coarse tremor, drowsiness; >2.0: ataxia, confusion, seizures; >2.5: life-threatening. Maintain adequate sodium and fluid intake (dehydration and low sodium increase lithium levels). Avoid NSAIDs, ACE inhibitors, thiazide diuretics (increase lithium levels). Monitor renal function, thyroid (causes hypothyroidism), pregnancy category D."),

        # Psych - Antipsychotics
        ("Typical vs atypical antipsychotics: Key differences and adverse effects?",
         "Typical/1st gen (haloperidol, chlorpromazine): block dopamine D2. High risk of EPS (dystonia → treat with benztropine/diphenhydramine, akathisia, parkinsonism, tardive dyskinesia — may be irreversible). Neuroleptic malignant syndrome (NMS): fever >104°F, muscle rigidity, altered LOC, elevated CK — stop drug, dantrolene, cooling. Atypical/2nd gen (risperidone, olanzapine, quetiapine, clozapine): fewer EPS but metabolic syndrome (weight gain, hyperglycemia, dyslipidemia). Clozapine: requires ANC monitoring (agranulocytosis risk)."),

        # Endocrine - Insulin Types (CORRECTED: clarified IV insulin)
        ("Rapid-acting insulins: Onset, peak, and duration?",
         "Lispro (Humalog), Aspart (NovoLog), Glulisine (Apidra). Onset: 10-15 min. Peak: 1-2 hrs. Duration: 3-5 hrs. Give within 15 min of eating. Clear solution. Only Regular insulin is used IV; rapid-acting insulins (lispro, aspart) are SubQ only. Used for mealtime coverage and correction doses. Highest hypoglycemia risk at peak time — ensure patient eats after injection."),

        ("Short-acting insulin (Regular/Novolin R): Onset, peak, and duration?",
         "Onset: 30 min. Peak: 2-4 hrs. Duration: 6-8 hrs. Give 30 min before meals. Clear solution. ONLY insulin given IV (for DKA, hyperkalemia). Used in sliding scales. Can be mixed with NPH (draw Regular first — 'clear before cloudy'). Monitor glucose and potassium (insulin shifts K+ intracellularly)."),

        # CORRECTED: NPH peak changed to 4-8 hours
        ("Intermediate-acting insulin (NPH): Onset, peak, and duration?",
         "NPH (Humulin N, Novolin N). Onset: 1-2 hrs. Peak: 4-8 hrs. Duration: 12-16 hrs. Cloudy solution — gently roll, do not shake. Can be mixed with Regular (draw Regular first). Given 1-2x daily. Unpredictable peak makes hypoglycemia risk variable. Never give IV. Often combined with rapid-acting for better coverage."),

        ("Long-acting insulins (glargine, detemir): Key characteristics?",
         "Glargine (Lantus, Basaglar): Onset 1-2 hrs, no peak (steady state), duration ~24 hrs. Detemir (Levemir): Onset 1-2 hrs, mild peak 6-8 hrs, duration 12-24 hrs. Both are clear solutions. Do NOT mix with other insulins. Given once or twice daily. Provide basal coverage. Glargine: acidic pH — do not mix (precipitates). Degludec (Tresiba): ultra-long-acting, duration >42 hrs."),

        # Endocrine - Metformin (CORRECTED: hold at time of contrast and 48 hrs AFTER)
        ("Metformin: Mechanism, key side effects, and contraindications?",
         "Biguanide — first-line for Type 2 DM. Decreases hepatic glucose production, increases insulin sensitivity. Does NOT cause hypoglycemia (when used alone). GI side effects common (start low, take with food). Serious risk: lactic acidosis — contraindicated if eGFR <30, active liver disease, heavy alcohol use. Hold at time of contrast and 48 hrs AFTER (current ACR guidelines). Monitor B12 (can cause deficiency with long-term use). No weight gain (may promote modest weight loss)."),

        # Endocrine - Levothyroxine
        ("Levothyroxine (Synthroid): Administration and monitoring?",
         "Synthetic T4 — hypothyroidism replacement. Take on empty stomach, 30-60 min before breakfast, with water only. Separate from calcium, iron, antacids by 4 hours (decrease absorption). Monitor TSH q6-8 weeks after dose changes. Goal TSH: 0.5-4.0 mIU/L. Narrow therapeutic index — maintain same brand. Toxicity signs = hyperthyroidism: tachycardia, weight loss, heat intolerance, tremor, insomnia. Requires lifelong therapy."),

        # Respiratory - Albuterol
        ("Albuterol: Classification, use, and side effects?",
         "Short-acting beta-2 agonist (SABA) — rescue inhaler for acute bronchospasm (asthma, COPD). Onset: 5-15 min. Duration: 4-6 hrs. Side effects: tachycardia, tremor, hypokalemia, nervousness. If using >2x/week for rescue, asthma is not well-controlled — step up therapy. Rinse mouth after use if using MDI. For nebulizer: 2.5 mg/3 mL. Using more than 1 canister/month indicates poor control."),

        # Respiratory - Ipratropium (CORRECTED: softened peanut/soy to caution)
        ("Ipratropium (Atrovent): Mechanism and use?",
         "Anticholinergic bronchodilator — blocks acetylcholine in bronchial smooth muscle. Used for COPD maintenance (less effective in asthma). Onset: 15-30 min. Duration: 4-6 hrs. Side effects: dry mouth, urinary retention, constipation, blurred vision. Use with caution in patients with soy or peanut allergy (MDI formulation contains soy lecithin; nebulizer solution does not). Often combined with albuterol (Combivent/DuoNeb). Not a rescue inhaler — slower onset than albuterol."),

        # Respiratory - Corticosteroids
        ("Inhaled corticosteroids (fluticasone, budesonide): Nursing considerations?",
         "Anti-inflammatory — cornerstone of persistent asthma maintenance. NOT for acute attacks. Rinse mouth and spit after each use to prevent oral candidiasis (thrush). Use spacer with MDI for better delivery. Side effects: hoarseness, oral thrush, pharyngitis. Systemic steroids (prednisone): taper if used >2 weeks — adrenal suppression. Monitor glucose, bone density, and growth in children with long-term use."),

        # GI - PPIs
        ("PPIs (omeprazole, pantoprazole): Mechanism and long-term risks?",
         "End in '-prazole.' Irreversibly block H+/K+ ATPase (proton pump) — most potent acid suppression. Take 30-60 min before first meal. Used for GERD, peptic ulcers, Zollinger-Ellison. Long-term risks (>1 year): C. diff infection, bone fractures (decreased calcium absorption), hypomagnesemia, vitamin B12 deficiency, kidney disease. FDA recommends shortest duration at lowest dose. Do not stop abruptly (rebound acid hypersecretion). IV pantoprazole for active GI bleed."),

        # GI - H2 Blockers
        ("H2 receptor blockers (famotidine, ranitidine): How do they differ from PPIs?",
         "End in '-tidine.' Block histamine H2 receptors on parietal cells — reduce acid secretion (less potent than PPIs). Famotidine (Pepcid): most commonly used (ranitidine/Zantac recalled for NDMA carcinogen). Faster onset than PPIs but shorter duration. Can be given IV. Fewer long-term risks than PPIs. Used for mild GERD, stress ulcer prophylaxis in ICU. Can cause headache, dizziness, constipation."),

        # GI - Antiemetics
        ("Ondansetron (Zofran): Mechanism, use, and key side effect?",
         "5-HT3 receptor antagonist — blocks serotonin in CTZ and vagal nerve. First-line antiemetic for chemotherapy, postoperative, and general N/V. Given IV, PO, or ODT (sublingual dissolving tab). Key side effect: QT prolongation — obtain baseline ECG in at-risk patients, avoid in patients with long QT syndrome. Other side effects: headache, constipation. Max IV dose: 16 mg (FDA). Serotonin syndrome risk with SSRIs (rare)."),

        ("Metoclopramide (Reglan): Use, mechanism, and black box warning?",
         "Dopamine antagonist — prokinetic (increases GI motility) and antiemetic. Used for gastroparesis, GERD, N/V. Black box warning: tardive dyskinesia with long-term use (>12 weeks) — may be irreversible. Can cause EPS (especially in young patients). Contraindicated in bowel obstruction, pheochromocytoma, seizure disorders. Give 30 min before meals. Monitor for involuntary movements."),

        # High-Alert Medications
        ("High-alert medications: What are they and what safety measures apply?",
         "Medications that carry heightened risk of significant harm if used in error. ISMP high-alert list includes: insulin, opioids, anticoagulants (heparin, warfarin), potassium chloride (IV), chemotherapy, neuromuscular blocking agents, concentrated electrolytes. Safety measures: independent double-check, barcode scanning, tall-man lettering, limit access to concentrated forms, standardized concentrations, smart pump drug libraries. Never abbreviate 'U' for units — write 'units.'"),

        ("ISMP 'Do Not Crush' list: Key examples and why?",
         "Never crush: enteric-coated (EC) tablets (destroy protective coating — GI irritation or inactivation), extended/sustained-release formulations (dose dumping — potential overdose), sublingual tabs (designed for buccal absorption), teratogenic drugs (exposure risk to handler). Examples: metoprolol succinate ER, oxycodone ER, omeprazole capsules (can open and sprinkle but not crush beads), potassium chloride ER. Always check before crushing; request liquid alternative if available."),

        # Additional Cardiac - Dopamine (CORRECTED: added note about renal-dose dopamine)
        ("Dopamine vs dobutamine: Key differences?",
         "Dopamine: dose-dependent effects — low dose (1-5 mcg/kg/min): renal vasodilation; moderate (5-10): increases cardiac output (beta-1); high (10-20): vasoconstriction (alpha). Note: Evidence does not support renal-dose dopamine for renal protection. Dobutamine: primarily beta-1 agonist — increases contractility without significant vasoconstriction. Used for acute heart failure. Both: continuous infusion only, central line preferred, monitor ECG continuously. Dobutamine can cause hypotension (vasodilation at higher doses)."),

        ("Atropine: Indications and nursing considerations?",
         "Anticholinergic — increases heart rate by blocking vagal tone. First-line for symptomatic bradycardia (0.5 mg IV q3-5 min, max 3 mg). Also used for organophosphate poisoning (high doses). Side effects: tachycardia, dry mouth, urinary retention, blurred vision, decreased GI motility. Contraindicated in narrow-angle glaucoma. In ACLS: used before transcutaneous pacing for unstable bradycardia."),

        # Additional Anticoagulant/Thrombolytic
        ("Alteplase (tPA): Indications, timing, and nursing care?",
         "Thrombolytic — converts plasminogen to plasmin, dissolves clots. Indications: acute ischemic stroke (within 4.5 hrs of onset), STEMI (if PCI not available), massive PE. Stroke dose: 0.9 mg/kg (max 90 mg) — 10% bolus, rest over 60 min. Contraindications: active bleeding, recent surgery (14 days), uncontrolled HTN (>185/110), INR >1.7, platelet <100,000. Nursing: neuro checks q15 min, no invasive procedures, monitor for bleeding, BP management, no anticoagulants for 24 hrs post."),

        # Additional Psych
        ("MAOIs (phenelzine, tranylcypromine): Critical dietary restriction?",
         "Monoamine oxidase inhibitors — rarely used, last-line antidepressants. CRITICAL: avoid tyramine-rich foods — aged cheese, cured meats, red wine, soy sauce, sauerkraut, tap/draft beer. Tyramine + MAOI = hypertensive crisis (severe headache, stiff neck, diaphoresis, BP >180/120 — can be fatal). Treat with phentolamine (alpha-blocker). Also avoid SSRIs, meperidine, pseudoephedrine (serotonin syndrome, hypertensive crisis). Washout period: 14 days before/after other antidepressants."),

        # Additional Endocrine
        ("Prednisone/corticosteroids: Systemic side effects and nursing considerations?",
         "Anti-inflammatory, immunosuppressive. Side effects (mnemonic: CUSHINGOID): Cataracts, Ulcers, Skin thinning/Striae, Hyperglycemia/HTN, Infections, Necrosis (avascular), Growth suppression, Osteoporosis, Immunosuppression, Diabetes/weight gain (buffalo hump, moon face). Take in AM (mimics cortisol rhythm). Take with food. Never stop abruptly if >2 weeks (adrenal crisis). Monitor glucose, K+, weight. Increase risk of infection — avoid live vaccines. Taper gradually."),

        ("Sliding scale insulin protocol: Key nursing actions?",
         "Regular insulin given based on blood glucose readings (typically q4-6h or AC/HS). Always verify: correct insulin type, correct dose per protocol, blood glucose value, and patient identity. Check glucose before meals and at bedtime. Hold and notify provider if glucose <70 mg/dL. Treat hypoglycemia with Rule of 15: 15g fast-acting carbs, recheck in 15 min. Document glucose and insulin given. Assess for signs of hypo (shakiness, diaphoresis, confusion) and hyperglycemia (polyuria, polydipsia, Kussmaul respirations in DKA)."),

        # Additional Safety
        ("Look-alike/sound-alike (LASA) medications: Key examples?",
         "Commonly confused pairs: hydrOXYzine (antihistamine) vs hydrALAZINE (antihypertensive), predniSONE vs prednisoLONE, metFORMIN vs metroNIDAZOLE, DOPamine vs DOBUTamine, ceREBYX (fosphenytoin) vs ceLEBREX (celecoxib), vinCRIStine (IV only) vs vinBLAStine. Prevention: use tall-man lettering, read labels carefully, barcode scanning, separate storage. VinCRIStine is FATAL if given intrathecally (IV only — must be in minibag per ISMP)."),

        ("Potassium chloride IV: Critical safety considerations?",
         "NEVER give IV push — fatal cardiac arrest. Always dilute: max concentration 40 mEq/L in peripheral line (up to 80 mEq/L central line with cardiac monitoring). Max rate: 10 mEq/hr peripheral (20 mEq/hr central with monitoring). Burns at infusion site — assess IV frequently. Must have adequate urine output (>0.5 mL/kg/hr) — kidneys excrete K+. Monitor ECG for tall peaked T waves (hyperkalemia). Verify serum K+ level before and after infusion."),

        # Additional
        ("Phenytoin (Dilantin): Therapeutic level, side effects, and IV safety?",
         "Anticonvulsant — narrow therapeutic index: 10–20 mcg/mL. IV: give slowly (max 50 mg/min) — only with NS (precipitates in dextrose). Monitor ECG and BP during IV infusion (risk of hypotension, bradycardia, cardiac arrest). Side effects: gingival hyperplasia (oral hygiene), hirsutism, nystagmus at toxic levels, ataxia, Stevens-Johnson syndrome. Many drug interactions (CYP450 inducer). Monitor free phenytoin if low albumin. Highly teratogenic."),

        ("Magnesium sulfate: Indications and toxicity monitoring?",
         "Indications: preeclampsia/eclampsia (seizure prophylaxis), torsades de pointes, severe hypomagnesemia. Therapeutic level: 4–7 mEq/L for preeclampsia. Toxicity progression: decreased DTRs (first sign — check patellar reflex) → respiratory depression → cardiac arrest. Monitor: DTRs, RR (hold if <12), urine output (>30 mL/hr — renally excreted), LOC. Antidote: calcium gluconate (1 g IV slow push). Keep at bedside. Continuous fetal monitoring in OB patients."),

        ("What are the 10 Rights of Medication Administration?",
         "1. Right patient (2 identifiers) 2. Right drug 3. Right dose 4. Right route 5. Right time 6. Right documentation 7. Right reason (indication) 8. Right response (evaluate effectiveness) 9. Right to refuse 10. Right education (teach patient about the medication). Always check allergies. Three safety checks: when pulling from drawer/Pyxis, when preparing, when at bedside before giving. If unsure, DO NOT GIVE — verify with pharmacy."),

        ("Epinephrine: Uses, routes, and dosing for anaphylaxis?",
         "Catecholamine — alpha and beta agonist. Anaphylaxis: 0.3-0.5 mg IM in anterolateral thigh (1:1,000 concentration = 1 mg/mL); pediatric: 0.01 mg/kg (max 0.3 mg). May repeat q5-15 min. EpiPen: adult 0.3 mg, junior 0.15 mg. Cardiac arrest (ACLS): 1 mg IV/IO q3-5 min (1:10,000 concentration). Also used for severe asthma, croup (racemic epi nebulizer). Side effects: tachycardia, hypertension, tremor, anxiety. Monitor ECG, BP. Never give 1:1,000 IV (use 1:10,000 for IV)."),

        ("Mannitol: Use, mechanism, and nursing considerations?",
         "Osmotic diuretic — increases serum osmolality, draws fluid from tissues (brain, eyes). Used for: increased intracranial pressure (ICP), acute glaucoma, cerebral edema. IV administration only — use filter needle (may crystallize). Monitor serum osmolality (hold if >320 mOsm/kg). Monitor I&O strictly (expect large urine output). Monitor electrolytes (hyponatremia, hypokalemia). Assess neuro status. Contraindicated in anuria, severe dehydration, active intracranial bleeding."),

        ("What is serotonin syndrome and which drug combinations cause it?",
         "Life-threatening condition from excess serotonergic activity. Triad: altered mental status (agitation, confusion), autonomic instability (hyperthermia, diaphoresis, tachycardia, BP changes), neuromuscular excitability (clonus, hyperreflexia, rigidity, tremor). Causes: combining SSRIs + MAOIs, SSRIs + tramadol, SSRIs + triptans, SSRIs + linezolid, meperidine + MAOIs. Treatment: stop offending agents, cyproheptadine (serotonin antagonist), benzodiazepines for agitation, cooling measures. Distinct from NMS (which involves dopamine blockade and lead-pipe rigidity)."),

        ("Nitroglycerin IV infusion: Key nursing points?",
         "Used for acute heart failure, unstable angina, hypertensive emergency. Must use glass bottles and non-PVC tubing (drug absorbs into PVC plastic, reducing delivered dose). Titrate to BP and chest pain relief. Monitor BP every 5-15 min during titration. Headache is expected (give acetaminophen). Maintain SBP >90. Use dedicated IV line if possible. Tolerance develops with continuous use. Wean gradually — do not stop abruptly."),

        ("Antifungal amphotericin B: Major toxicities and nursing care?",
         "Called 'ampho-terrible' due to severe side effects. Major toxicity: nephrotoxicity (monitor BUN/Cr, I&O — prehydrate with NS). Infusion reactions: fever, chills, rigors, N/V (premedicate with acetaminophen, diphenhydramine, meperidine for rigors). Hypokalemia, hypomagnesemia (replace electrolytes). Anemia with prolonged use. Liposomal formulation (AmBisome) has fewer side effects. Test dose may be given first. Infuse slowly over 2-6 hours."),
    ]
  },
  {
    "slug": "nursing-cardiac-respiratory",
    "title": "Cardiac & Respiratory Nursing",
    "category": "Professional",
    "description": "Comprehensive cardiac and respiratory nursing flashcards covering heart failure, MI, EKG, chest tubes, ABGs, oxygen therapy, and mechanical ventilation.",
    "meta_desc": "Free cardiac and respiratory nursing flashcards. 50 cards covering heart failure, MI, EKG, ABGs, chest tubes, oxygen delivery, COPD, asthma, and ventilator care.",
    "keywords": "cardiac nursing flashcards, respiratory nursing flashcards, NCLEX cardiac, nursing EKG cards, ABG interpretation flashcards",
    "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
    "cards": [
        # Heart Failure
        ("Left-sided heart failure: Key symptoms and pathophysiology?",
         "Left ventricle fails to pump blood forward → blood backs up into pulmonary circulation. Symptoms: dyspnea, orthopnea, paroxysmal nocturnal dyspnea (PND), crackles/rales on auscultation, pink frothy sputum (pulmonary edema), tachycardia, S3 gallop, fatigue, decreased urine output. Elevated BNP (>100 pg/mL). CXR: pulmonary congestion, cardiomegaly. Most common cause: CAD, hypertension. Think 'Left = Lung.'"),

        ("Right-sided heart failure: Key symptoms and common cause?",
         "Right ventricle fails → blood backs up into systemic venous circulation. Symptoms: jugular venous distension (JVD), peripheral/dependent edema, ascites, hepatomegaly (liver engorgement), weight gain, anorexia/nausea. Most common cause: LEFT-sided heart failure. Other causes: COPD (cor pulmonale), PE, pulmonic stenosis. Treatment: diuretics, fluid/sodium restriction, ACE inhibitors/ARBs, beta-blockers, daily weights. Think 'Right = Rest of body.'"),

        ("Heart failure nursing interventions and patient teaching?",
         "Daily weights (same time, same scale — report gain >2 lbs/day or 5 lbs/week). Low sodium diet (<2 g/day). Fluid restriction (1.5-2 L/day if severe). I&O monitoring. Elevate HOB. O2 as needed. Medications: ACE inhibitors, beta-blockers (carvedilol, metoprolol succinate), diuretics, digoxin, aldosterone antagonists (spironolactone). Activity: regular low-intensity exercise as tolerated. Teach: monitor for edema, weigh daily, report dyspnea, medication compliance, avoid NSAIDs (fluid retention)."),

        # MI
        ("Acute MI: Assessment findings and immediate interventions?",
         "Assessment: crushing substernal chest pain (may radiate to jaw, left arm, back), diaphoresis, N/V, dyspnea, anxiety, denial. Women/diabetics/elderly: may present atypically (fatigue, indigestion, jaw pain). ECG: ST elevation (STEMI) or depression (NSTEMI), T-wave inversion. Troponin elevated (rises 3-6 hrs, peaks 12-24 hrs). Immediate interventions — MONA (modified): Morphine (if pain unrelieved), Oxygen (only if SpO2 <94%), Nitroglycerin (SL), Aspirin (162-325 mg chewed). Activate cath lab for STEMI (door-to-balloon <90 min)."),

        ("Post-MI nursing care and complications?",
         "Bed rest → progressive activity. Continuous cardiac monitoring (watch for arrhythmias — #1 cause of death in first 24 hrs). Serial troponins and ECGs. Medications: dual antiplatelet therapy (aspirin + P2Y12 inhibitor), statin, ACE inhibitor, beta-blocker. Monitor for complications: cardiogenic shock, heart failure, ventricular arrhythmias, papillary muscle rupture (new murmur), ventricular septal defect, Dressler syndrome (pericarditis weeks later), cardiac tamponade. Cardiac rehab referral. Teach: lifestyle modification, when to call 911."),

        # EKG Basics
        ("Normal sinus rhythm: Criteria on ECG?",
         "Rate: 60-100 bpm. Regular rhythm. P wave before every QRS, QRS after every P. P-R interval: 0.12-0.20 sec (3-5 small boxes). QRS duration: <0.12 sec (<3 small boxes). Each small box = 0.04 sec, each large box = 0.20 sec. P waves upright and uniform in Lead II. Isoelectric baseline between beats. Calculating rate: 300 / # of large boxes between R-R intervals (regular rhythm) or count R waves in 6-second strip x 10 (irregular rhythm)."),

        ("Atrial fibrillation: ECG characteristics and management?",
         "ECG: irregularly irregular rhythm, no identifiable P waves (fibrillatory baseline), variable R-R intervals, narrow QRS (unless aberrant conduction). Rate: can be rapid (>100 = afib with RVR) or controlled. Risk: blood stasis in atria → thrombus → stroke. Management: rate control (beta-blocker, diltiazem, digoxin), rhythm control (amiodarone, cardioversion), anticoagulation (CHA2DS2-VASc score determines need — DOACs or warfarin). If onset <48 hrs: may cardiovert. If >48 hrs: anticoagulate 3 weeks before cardioversion or rule out clot with TEE."),

        ("Ventricular tachycardia vs ventricular fibrillation: Recognition and treatment?",
         "V-Tach: wide QRS (>0.12 sec), regular, rate 150-250 bpm, no identifiable P waves. If pulseless: treat as Vfib (defibrillation). If pulse present: stable → amiodarone or lidocaine; unstable → synchronized cardioversion. V-Fib: chaotic, no organized rhythm, no identifiable waves, no pulse. Immediately fatal if untreated. Treatment: CPR + defibrillation (unsynchronized shock) ASAP. ACLS: CPR → shock → epinephrine 1 mg q3-5 min → shock → amiodarone 300 mg → shock → amiodarone 150 mg. Continue CPR between interventions."),

        ("Heart blocks: First, second (Type I and II), and third degree?",
         "1st degree: prolonged PR interval >0.20 sec, all P waves conducted — benign, monitor only. 2nd degree Type I (Wenckebach): progressive PR prolongation until a QRS is dropped — usually benign. 2nd degree Type II (Mobitz II): constant PR interval with suddenly dropped QRS — dangerous, may progress to 3rd degree, may need pacemaker. 3rd degree (complete): no relationship between P waves and QRS complexes (AV dissociation) — atria and ventricles beat independently. Requires transcutaneous pacing → permanent pacemaker. Treat symptomatic bradycardia with atropine first."),

        # Cardiac Cath
        ("Cardiac catheterization: Pre-procedure and post-procedure nursing care?",
         "Pre: assess allergies (contrast dye, shellfish/iodine — may need premedication), NPO 6-8 hrs, baseline peripheral pulses (mark with marker), labs (BUN/Cr — contrast is nephrotoxic, PT/INR), consent, IV access, remove jewelry. Post: bedrest with affected extremity straight (femoral: 4-6 hrs; radial: 1-2 hrs). Monitor: site for bleeding/hematoma (apply pressure if bleeding), circulation of affected limb (5 P's: pain, pallor, pulselessness, paresthesia, paralysis), VS q15 min x 4 → q30 min x 2 → q1h. Hydrate to flush contrast (monitor I&O). Report: chest pain, back pain (retroperitoneal bleed), loss of pulse."),

        # Valve Disorders
        ("Mitral stenosis vs mitral regurgitation: Key differences?",
         "Mitral stenosis: narrowed mitral valve → impaired filling of LV. Causes: rheumatic heart disease (#1). Symptoms: dyspnea, fatigue, afib, hemoptysis, rumbling diastolic murmur. Mitral regurgitation: mitral valve doesn't close fully → blood leaks back to LA during systole. Causes: MI (papillary muscle dysfunction), endocarditis, mitral valve prolapse. Symptoms: dyspnea, fatigue, high-pitched blowing systolic murmur radiating to axilla. Both lead to left atrial enlargement → pulmonary congestion → right heart failure eventually. Treatment: medical management, valve repair/replacement."),

        ("Aortic stenosis: Assessment and nursing considerations?",
         "Narrowed aortic valve → LV outflow obstruction. Classic triad: syncope, angina, dyspnea on exertion. Harsh systolic crescendo-decrescendo murmur at right upper sternal border, radiating to carotids. Causes: calcific degeneration (elderly), bicuspid valve (younger). Leads to LV hypertrophy → heart failure. Avoid strenuous activity (risk of sudden death). Monitor for heart failure symptoms. Treatment: surgical aortic valve replacement (SAVR) or transcatheter (TAVR). Post-valve replacement: anticoagulation (mechanical valve: lifelong warfarin, INR 2.5-3.5; bioprosthetic: short-term)."),

        # Hypertension
        ("Hypertension: Classifications and nursing management?",
         "Normal: <120/80. Elevated: 120-129/<80. Stage 1 HTN: 130-139 or 80-89. Stage 2 HTN: >=140 or >=90. Hypertensive crisis: >180/120. Management: lifestyle first (DASH diet, sodium <2.3 g/day, exercise 150 min/week, limit alcohol, weight loss, smoking cessation). Medications: Stage 1: thiazide diuretic, ACE/ARB, or CCB. Stage 2: two-drug combination. African American patients: CCB or thiazide preferred initially. Diabetic or CKD: ACE or ARB (renoprotective). Teach: BP monitoring, medication compliance (no symptoms doesn't mean stop meds), avoid NSAIDs."),

        ("Hypertensive crisis: Emergency vs urgency and treatment?",
         "Both: BP >180/120. Hypertensive urgency: severely elevated BP WITHOUT target organ damage (headache, anxiety). Lower BP gradually over 24-48 hrs with oral meds. Hypertensive emergency: severely elevated BP WITH target organ damage (encephalopathy, stroke, MI, aortic dissection, pulmonary edema, acute kidney injury). Requires ICU, IV meds (nitroprusside, labetalol, nicardipine, nitroglycerin). Lower MAP by no more than 25% in first hour (too rapid → stroke, MI). Arterial line for continuous BP monitoring. Neuro checks frequently."),

        # Chest Tubes (CORRECTED: ALL 4 sides with petroleum gauze)
        ("Chest tube management: Key nursing considerations?",
         "Indications: pneumothorax, hemothorax, pleural effusion, post-thoracic surgery. System: collection chamber, water seal chamber (2 cm H2O — should see tidaling with respirations; continuous bubbling = air leak), suction control chamber. Nursing care: keep system below chest level, maintain airtight connections, never clamp except for brief assessment, encourage coughing and deep breathing. Monitor drainage: report >100 mL/hr (hemorrhage). Assess for subcutaneous emphysema (crepitus). If disconnected: place tube end in sterile water. If pulled out: cover site immediately with petroleum gauze occlusive dressing taped on ALL 4 sides. Document drainage amount, color, and character."),

        ("Chest tube: When to notify the provider?",
         "Notify provider: drainage >100 mL/hr (hemorrhage), continuous bubbling in water seal chamber (persistent air leak), sudden cessation of drainage (possible clot/kink), subcutaneous emphysema increasing, signs of tension pneumothorax (tracheal deviation, absent breath sounds, hypotension, JVD), patient develops respiratory distress, change in drainage color (bloody → serous is expected; sudden return to bloody is not). After removal: monitor for recurrent pneumothorax (dyspnea, decreased breath sounds, CXR). Chest tube removal: end of expiration or during Valsalva maneuver."),

        # Oxygen Delivery
        ("Oxygen delivery systems: Flow rates and FiO2?",
         "Low-flow systems: Nasal cannula: 1-6 L/min (FiO2 ~24-44%, adds ~4% per liter). Simple face mask: 5-8 L/min (FiO2 40-60%) — minimum 5 L/min to prevent CO2 rebreathing. Partial rebreather: 6-15 L/min (FiO2 60-75%). Non-rebreather: 10-15 L/min (FiO2 80-95%) — keep reservoir bag inflated. High-flow systems: Venturi mask: precise FiO2 (24-50%) — best for COPD. High-flow nasal cannula (HFNC): up to 60 L/min, FiO2 21-100%."),

        ("CPAP vs BiPAP: Differences and indications?",
         "CPAP (Continuous Positive Airway Pressure): delivers constant pressure during inhalation AND exhalation. Keeps alveoli open. Indications: obstructive sleep apnea, acute pulmonary edema. One pressure setting. BiPAP (Bilevel Positive Airway Pressure): delivers higher pressure on inhalation (IPAP) and lower on exhalation (EPAP). Easier to exhale against. Indications: COPD exacerbation, neuromuscular disease, sleep apnea intolerant of CPAP. Both are non-invasive ventilation. Contraindications: unprotected airway, facial trauma, vomiting, hemodynamic instability. Monitor for gastric distension, skin breakdown from mask."),

        # ABGs
        ("ABG interpretation: Normal values and systematic approach?",
         "Normal values: pH 7.35-7.45, PaCO2 35-45 mmHg, HCO3 22-26 mEq/L, PaO2 80-100 mmHg, SaO2 >95%. Step 1: Look at pH (acidosis <7.35 or alkalosis >7.45). Step 2: Check PaCO2 — if abnormal and matches the pH direction, respiratory cause (CO2 is acid — high CO2 = acidosis). Step 3: Check HCO3 — if abnormal and matches pH direction, metabolic cause (HCO3 is base — low HCO3 = acidosis). Step 4: Check compensation — the other system will move to try to normalize pH. Partially compensated: pH still abnormal. Fully compensated: pH normal (look at which value moved first to determine primary cause)."),

        # CORRECTED: Added V/Q mismatch note for COPD
        ("Respiratory acidosis: Causes, ABG findings, and treatment?",
         "ABG: pH <7.35, PaCO2 >45 mmHg (elevated CO2 retained). Cause: hypoventilation — CO2 not being blown off. Common causes: COPD, sedation/opioids, neuromuscular disease, pneumonia, airway obstruction, respiratory failure. Compensation: kidneys retain HCO3 (takes 24-48 hrs). Treatment: improve ventilation — bronchodilators, reverse sedation (naloxone), BiPAP/CPAP, intubation if severe. For COPD patients: low-flow O2 (1-2 L). Note: The traditional 'hypoxic drive' theory is largely outdated; the actual mechanism of O2-induced hypercapnia in COPD is worsening V/Q mismatch and the Haldane effect."),

        ("Respiratory alkalosis: Causes, ABG findings, and treatment?",
         "ABG: pH >7.45, PaCO2 <35 mmHg (too much CO2 blown off). Cause: hyperventilation — anxiety/panic attacks, pain, fever, early sepsis, PE, high altitude, mechanical ventilation (rate too high). Compensation: kidneys excrete HCO3 (takes 24-48 hrs). Treatment: treat underlying cause. Anxiety: coaching to slow breathing, rebreathing into paper bag (controversial), anxiolytics. Mechanical vent: decrease rate or tidal volume. Monitor for tetany, numbness/tingling (alkalosis decreases ionized calcium)."),

        ("Metabolic acidosis: Causes (MUDPILES) and treatment?",
         "ABG: pH <7.35, HCO3 <22 mEq/L. Causes — MUDPILES: Methanol, Uremia, DKA, Propylene glycol, Isoniazid/Iron, Lactic acidosis, Ethylene glycol, Salicylates. Also: severe diarrhea (loss of bicarb), renal failure. Compensation: Kussmaul respirations (deep, rapid breathing to blow off CO2). Treatment: treat underlying cause (insulin for DKA, dialysis for uremia), sodium bicarbonate if pH <7.1 (severe), fluid resuscitation. Monitor potassium (acidosis shifts K+ out of cells — may appear normal but drop rapidly with treatment)."),

        ("Metabolic alkalosis: Causes and treatment?",
         "ABG: pH >7.45, HCO3 >26 mEq/L. Causes: prolonged vomiting or NG suction (loss of HCl), excessive antacid use, excessive NaHCO3 administration, hypokalemia (kidneys retain H+ to excrete K+), loop/thiazide diuretics, Cushing syndrome. Compensation: slow, shallow respirations (retain CO2). Treatment: treat underlying cause, replace potassium and chloride (normal saline with KCl), antiemetics for vomiting, discontinue offending meds. Monitor for hypokalemia, hypocalcemia (increased neuromuscular excitability)."),

        # Pneumonia
        ("Pneumonia: Assessment, types, and nursing management?",
         "Assessment: productive cough (rust-colored sputum = pneumococcal), fever/chills, dyspnea, tachypnea, pleuritic chest pain, crackles on auscultation, dullness to percussion (consolidation). Types: community-acquired (CAP) — S. pneumoniae #1 cause; hospital-acquired (HAP) — onset >48 hrs after admission; ventilator-associated (VAP). Diagnostics: CXR (infiltrate), sputum C&S, CBC (elevated WBC), blood cultures. Nursing: O2 therapy, antibiotics (obtain cultures BEFORE first dose), encourage fluids, incentive spirometry, HOB elevated, isolation if needed (TB: airborne). Prevention: pneumococcal vaccine, flu vaccine, hand hygiene."),

        # COPD (CORRECTED: added V/Q mismatch note about hypoxic drive)
        ("COPD: Pathophysiology, assessment, and management?",
         "Chronic bronchitis + emphysema. Chronic bronchitis: 'blue bloater' — productive cough, hypoxemia, cyanosis, cor pulmonale. Emphysema: 'pink puffer' — barrel chest, pursed-lip breathing, dyspnea, thin, uses accessory muscles. Both: irreversible airflow limitation. Assessment: decreased breath sounds, wheezing, prolonged expiration, hyperinflation on CXR. Management: smoking cessation (#1 intervention), bronchodilators (SABA rescue + LAMA maintenance +/- LABA +/- ICS), pulmonary rehab, O2 therapy (low flow 1-2 L/min — titrate to SpO2 88-92%), flu + pneumococcal vaccines. O2 CAUTION: The hypoxic drive theory is largely outdated; the actual mechanism of O2-induced hypercapnia in COPD is V/Q mismatch worsening and the Haldane effect. Still use low-flow O2 and titrate carefully."),

        # Asthma
        ("Asthma: Assessment, acute management, and status asthmaticus?",
         "Assessment: wheezing (expiratory initially → may become silent if severe = ominous sign), dyspnea, chest tightness, cough (especially nocturnal), tachypnea, use of accessory muscles. Triggers: allergens, exercise, cold air, infection, stress. Acute management: SABA (albuterol) first-line + ipratropium for severe exacerbation + systemic corticosteroids (prednisone or methylprednisolone) + O2 to maintain SpO2 >90%. Maintenance: ICS (fluticasone) +/- LABA (salmeterol). Status asthmaticus: life-threatening, not responding to initial treatment — may need IV magnesium sulfate (bronchodilator), heliox, intubation. Monitor peak flow: <50% of personal best = severe."),

        # PE
        ("Pulmonary embolism: Assessment, diagnosis, and management?",
         "Risk factors: Virchow's triad — venous stasis, hypercoagulability, endothelial injury. DVT, immobility, surgery, OCP use, malignancy, obesity. Assessment: sudden dyspnea (most common), pleuritic chest pain, tachycardia, tachypnea, anxiety, hypoxemia, possible hemoptysis, JVD. ABG: respiratory alkalosis (early). Diagnosis: CT pulmonary angiography (gold standard), D-dimer (sensitive but not specific — rules out if negative), V/Q scan if CT contraindicated. Management: anticoagulation (heparin → warfarin or DOAC), thrombolytics (alteplase) for massive PE with hemodynamic instability, IVC filter if anticoagulation contraindicated. Prevention: early ambulation, SCDs, DVT prophylaxis."),

        # Mechanical Ventilation
        ("Mechanical ventilation: Key settings and nursing considerations?",
         "Settings: FiO2 (21-100% — wean to <60% ASAP to prevent O2 toxicity), Tidal Volume (6-8 mL/kg ideal body weight — lung-protective), RR (12-20), PEEP (Positive End-Expiratory Pressure — keeps alveoli open, improves oxygenation, typically 5 cm H2O). Modes: Assist-Control (AC): vent delivers set rate + assists patient-initiated breaths. SIMV: set rate + patient breathes independently between vent breaths (used for weaning). Pressure Support: augments spontaneous breaths only. Nursing: HOB 30-45 degrees (prevent VAP), oral care q2h with chlorhexidine, sedation vacation daily, spontaneous breathing trial (SBT) assessment, monitor ABGs, alarm settings ON, secure ETT (note cm mark at lip), suction PRN."),

        # CORRECTED: Trach cuff pressure changed to 20-30 cm H2O
        ("Ventilator-associated pneumonia (VAP) prevention bundle?",
         "VAP bundle: HOB elevation 30-45 degrees, daily sedation vacation and assess readiness to extubate, DVT prophylaxis, PUD/stress ulcer prophylaxis (PPI or H2 blocker), oral care with chlorhexidine 0.12% q2-4 hrs, hand hygiene, subglottic suctioning (if available), avoid unnecessary circuit changes, maintain ETT cuff pressure 20-30 cm H2O. Diagnosis: new or progressive infiltrate on CXR + fever + purulent secretions + elevated WBC. Treatment: empiric broad-spectrum antibiotics → narrow based on sputum cultures."),

        # Additional Cardiac Content
        ("Cardiac tamponade: Assessment and Beck's triad?",
         "Fluid accumulation in pericardial sac → compresses heart → decreased cardiac output. Beck's Triad: hypotension, muffled/distant heart sounds, JVD. Also: tachycardia, pulsus paradoxus (>10 mmHg drop in SBP during inspiration), narrowed pulse pressure, anxiety, dyspnea. Diagnosis: echocardiogram. Emergency treatment: pericardiocentesis (needle aspiration of pericardial fluid). Keep patient upright to pool fluid away from heart. Causes: trauma, post-cardiac surgery, MI (ventricular rupture), pericarditis, malignancy."),

        ("Pericarditis: Assessment and nursing management?",
         "Inflammation of pericardium. Assessment: sharp, pleuritic chest pain that worsens with inspiration and lying flat, IMPROVES with sitting up and leaning forward (key distinguishing feature from MI). Pericardial friction rub on auscultation (scratchy, high-pitched sound). ECG: diffuse ST elevation (concave up — saddle-shaped), PR depression. Diagnosis: echo (may show effusion), elevated ESR/CRP. Treatment: NSAIDs (ibuprofen) + colchicine (reduces recurrence). Avoid anticoagulants (risk of hemopericardium). Monitor for cardiac tamponade (complication)."),

        ("Endocarditis: Risk factors, assessment, and Duke criteria?",
         "Infection of heart valves/endocardium. Risk factors: IV drug use (tricuspid valve), prosthetic valves, dental procedures, congenital heart defects, poor dentition. Common organisms: S. aureus (#1), Streptococcus viridans (dental). Assessment: persistent fever, new or changing murmur, Janeway lesions (painless red spots on palms/soles), Osler nodes (painful nodules on fingers/toes), Roth spots (retinal hemorrhages), splinter hemorrhages (nails), splenomegaly, petechiae. Diagnosis: Duke criteria — positive blood cultures (draw 3 sets before antibiotics) + echo findings (vegetations). Treatment: IV antibiotics 4-6 weeks. Teach: prophylactic antibiotics before dental procedures for high-risk patients."),

        ("Aortic aneurysm: Types, assessment, and nursing care?",
         "Thoracic aortic aneurysm (TAA) or abdominal aortic aneurysm (AAA). AAA: pulsatile abdominal mass (DO NOT palpate vigorously), bruit, back/flank/abdominal pain (if rupturing). Screen: one-time ultrasound for men aged 65-75 who ever smoked. Dissecting aneurysm: tearing/ripping pain radiating to back, BP difference between arms >20 mmHg, diaphoresis, hypertension. Nursing: strict BP control (SBP <120, HR <60 — IV labetalol, nitroprusside), pain management, prepare for emergency surgery if rupturing (cross-match blood, large-bore IVs, consent). Monitor hemoglobin, renal function. Post-op: monitor graft site, peripheral pulses, neuro checks (spinal cord perfusion)."),

        # Additional Respiratory
        # CORRECTED: Tracheostomy — normal saline only, cuff pressure 20-30
        ("Tracheostomy care: Key nursing considerations?",
         "Keep trach ties secure (1-2 finger breadth looseness). Clean inner cannula q8h or PRN (or replace if disposable). Trach care: clean stoma site with normal saline only (H2O2 is no longer recommended), apply pre-cut gauze (never cut gauze — loose threads can be aspirated). Keep obturator at bedside (for reinsertion). Keep same-size and one-size-smaller trach at bedside. Suctioning: preoxygenate with 100% O2, sterile technique, insert without suction, apply suction on withdrawal (max 10-15 seconds), max 3 passes. Cuff: keep 20-30 cm H2O (check with manometer). Accidental decannulation: <7 days post-op = surgical emergency (stoma may close); >7 days = reinsert or ventilate via stoma."),

        ("Tension pneumothorax: Assessment and emergency treatment?",
         "Air enters pleural space but cannot escape → pressure builds → mediastinal shift → compresses opposite lung and heart. Assessment: severe dyspnea, tracheal deviation (away from affected side), absent breath sounds on affected side, JVD, hypotension, tachycardia, cyanosis, hyperresonance to percussion. EMERGENCY treatment: needle decompression — large-bore needle (14-16 gauge) at 2nd intercostal space, midclavicular line on affected side → followed by chest tube placement. Do NOT wait for CXR if clinical signs are present and patient is unstable. Causes: trauma, barotrauma from mechanical ventilation, central line insertion."),

        ("ARDS (Acute Respiratory Distress Syndrome): Criteria and management?",
         "Non-cardiogenic pulmonary edema with diffuse alveolar damage. Berlin criteria: acute onset (within 1 week), bilateral opacities on CXR (white-out), PaO2/FiO2 ratio <=300 (mild <=300, moderate <=200, severe <=100), not fully explained by heart failure. Causes: sepsis (#1), pneumonia, aspiration, trauma, pancreatitis. Management: lung-protective ventilation (low tidal volume 6 mL/kg, PEEP optimization), prone positioning (16+ hrs/day — improves oxygenation), conservative fluid management, neuromuscular blockade if severe, treat underlying cause. Nursing: continuous SpO2/hemodynamic monitoring, oral care, DVT/stress ulcer prophylaxis, nutrition, skin assessment when prone."),

        ("Tuberculosis: Testing, transmission, and nursing management?",
         "Caused by Mycobacterium tuberculosis. Transmission: airborne droplet nuclei. Testing: Mantoux (TST/PPD) — read in 48-72 hrs, measure induration (not redness): >=5 mm positive (HIV, close contacts, CXR changes), >=10 mm (high-risk groups — immigrants, healthcare workers, IV drug users), >=15 mm (no risk factors). Positive PPD → CXR. QuantiFERON-TB Gold (blood test) — preferred in BCG-vaccinated. Isolation: airborne precautions (negative-pressure room, N95 respirator, patient wears surgical mask during transport). Treatment: RIPE therapy — Rifampin (orange body fluids, drug interactions), Isoniazid (INH — give with vitamin B6/pyridoxine to prevent peripheral neuropathy, hepatotoxic), Pyrazinamide, Ethambutol (monitor vision — optic neuritis). Duration: 6-9 months. Monitor LFTs."),

        ("Pulmonary function tests: Key values and their meaning?",
         "FEV1 (Forced Expiratory Volume in 1 sec): amount exhaled in first second — decreased in obstructive disease (COPD, asthma). FVC (Forced Vital Capacity): total amount exhaled — decreased in restrictive disease (pulmonary fibrosis). FEV1/FVC ratio: <70% = obstructive disease; normal or increased in restrictive disease. Peak Expiratory Flow Rate (PEFR): effort-dependent, used for asthma monitoring (green >80%, yellow 50-80%, red <50% of personal best). TLC (Total Lung Capacity): increased in COPD (air trapping), decreased in restrictive disease."),

        ("Oxygen toxicity: When does it occur and how to prevent?",
         "Occurs when FiO2 >60% for prolonged periods (>24-48 hrs). Pathophysiology: high O2 concentrations generate free radicals → damage alveolar-capillary membrane → inflammation, atelectasis (absorption atelectasis — nitrogen washout), ARDS-like picture. Signs: substernal chest pain, cough, dyspnea, decreased lung compliance. Prevention: use lowest FiO2 to maintain adequate oxygenation (SpO2 >=92% or PaO2 >=60 mmHg), wean FiO2 as tolerated, use PEEP to allow lower FiO2. Special populations: neonates — retinopathy of prematurity (ROP) with excessive O2; COPD — target SpO2 88-92%."),

        ("Synchronized cardioversion vs defibrillation: Key differences?",
         "Cardioversion: synchronized shock — machine senses R wave and delivers shock during QRS (avoids R-on-T phenomenon → Vfib). Used for unstable tachyarrhythmias WITH a pulse (afib, aflutter, SVT, Vtach with pulse). Sedation required (patient is conscious). Start at lower energy. Defibrillation: unsynchronized shock — delivers immediately regardless of cardiac cycle. Used for pulseless Vtach and Vfib ONLY. No sedation (patient is pulseless). Start at manufacturer-recommended energy (biphasic: 120-200J). If a synchronized shock is attempted on Vfib, the machine may not fire (no R wave to sync to)."),

        ("Coronary artery bypass graft (CABG): Post-op nursing care?",
         "Immediate post-op: ICU, intubated on ventilator, hemodynamic monitoring (arterial line, PA catheter, CVP). Chest tubes (mediastinal and/or pleural). Monitor for: bleeding (>100 mL/hr x 3 hrs), cardiac tamponade, arrhythmias (afib most common post-CABG), MI, infection. Assess neurological status (stroke risk from bypass). Sternal precautions: no pushing/pulling >10 lbs for 6-8 weeks, hug pillow when coughing, no driving for 4-6 weeks. Leg incision care (if saphenous vein graft) — monitor for swelling, elevate leg. Assess peripheral pulses. Incentive spirometry q1h while awake. Progressive ambulation. Cardiac rehab referral."),

        ("Electrocardiogram leads: Placement and what each lead views?",
         "12-lead ECG views the heart from 12 angles. Limb leads: I, II, III, aVR, aVL, aVF. Precordial leads: V1-V6. Leads II, III, aVF = inferior wall (RCA). Leads V1-V4 = anterior wall (LAD). Leads I, aVL, V5, V6 = lateral wall (LCx). Leads V1-V2 = septal wall. V3-V4 = anterior. Reciprocal changes (ST depression) appear in leads opposite the infarct. Right-sided leads (V4R) for right ventricular MI (avoid nitroglycerin and morphine — preload dependent). Posterior MI: tall R waves and ST depression in V1-V3 (mirror image)."),

        ("Hemodynamic monitoring: Normal values for CVP, PAP, PCWP, CO, SVR?",
         "CVP (Central Venous Pressure/Right Atrial Pressure): 2-8 mmHg — reflects right heart preload. Elevated: right heart failure, fluid overload. Low: hypovolemia. PAP (Pulmonary Artery Pressure): systolic 15-30, diastolic 4-12, mean 9-18 mmHg. PCWP (Pulmonary Capillary Wedge Pressure): 6-12 mmHg — reflects left heart preload. Elevated >18: left heart failure, fluid overload. CO (Cardiac Output): 4-8 L/min. CI (Cardiac Index): 2.5-4.0 L/min/m2. SVR (Systemic Vascular Resistance): 800-1200 dynes/sec/cm-5. Cardiogenic shock: high PCWP, low CO, high SVR. Septic shock (warm phase): low SVR, high CO, low PCWP."),
    ]
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

print(f"\nGenerated {len(DECKS)} nursing deck pages")
