#!/usr/bin/env python3
"""Generate individual deck HTML pages from deck data."""
import json, html, uuid, os

SITE = "/Users/stephaniedugas/Documents/stacked-site"

DECKS = [
  {
    "slug": "sat-vocabulary",
    "title": "SAT Vocabulary",
    "category": "Test Prep",
    "description": "Essential SAT vocabulary words with definitions. Master these high-frequency words to boost your verbal score.",
    "meta_desc": "Free SAT vocabulary flashcards. 50 essential high-frequency SAT words with definitions. Study online or import into the Stacked app instantly.",
    "keywords": "SAT vocabulary, SAT vocab flashcards, SAT words, SAT prep, SAT study cards",
    "color": {"hex": "#007AFF", "r": 0.0, "g": 0.478, "b": 1.0},
    "cards": [
      ("Aberration", "A departure from what is normal or expected"),
      ("Abscond", "To leave hurriedly and secretly to escape detection"),
      ("Acumen", "The ability to make good judgments and quick decisions"),
      ("Admonish", "To warn or reprimand firmly"),
      ("Aesthetic", "Concerned with beauty or the appreciation of beauty"),
      ("Ambiguous", "Open to more than one interpretation; unclear"),
      ("Ameliorate", "To make something bad or unsatisfactory better"),
      ("Anachronism", "Something belonging to a different time period"),
      ("Antipathy", "A deep-seated feeling of dislike or aversion"),
      ("Apathy", "Lack of interest, enthusiasm, or concern"),
      ("Arcane", "Understood by few; mysterious or secret"),
      ("Arduous", "Involving or requiring strenuous effort; difficult"),
      ("Articulate", "Having or showing the ability to speak fluently and clearly"),
      ("Audacious", "Showing a willingness to take bold risks"),
      ("Auspicious", "Conducive to success; favorable"),
      ("Benevolent", "Well-meaning and kindly; generous"),
      ("Bolster", "To support or strengthen; to prop up"),
      ("Cacophony", "A harsh, discordant mixture of sounds"),
      ("Candid", "Truthful and straightforward; frank"),
      ("Capricious", "Given to sudden and unaccountable changes of mood"),
      ("Cogent", "Clear, logical, and convincing"),
      ("Complacent", "Showing smug or uncritical satisfaction with oneself"),
      ("Concede", "To admit that something is true after first resisting"),
      ("Conundrum", "A confusing and difficult problem or question"),
      ("Corroborate", "To confirm or give support to a statement or theory"),
      ("Credulous", "Having or showing too great a readiness to believe things"),
      ("Debilitate", "To make someone weak and infirm"),
      ("Deference", "Humble submission and respect"),
      ("Deleterious", "Causing harm or damage"),
      ("Diligent", "Having or showing care in one's work or duties"),
      ("Discern", "To perceive or recognize something"),
      ("Eloquent", "Fluent or persuasive in speaking or writing"),
      ("Emulate", "To match or surpass by imitation"),
      ("Enigma", "A person or thing that is mysterious or puzzling"),
      ("Ephemeral", "Lasting for a very short time"),
      ("Equivocal", "Open to more than one interpretation; ambiguous"),
      ("Erratic", "Not even or regular in pattern; unpredictable"),
      ("Exacerbate", "To make a problem or situation worse"),
      ("Fastidious", "Very attentive to detail; meticulous"),
      ("Fervent", "Having or displaying passionate intensity"),
      ("Frivolous", "Not having any serious purpose or value"),
      ("Gregarious", "Fond of company; sociable"),
      ("Hackneyed", "Lacking significance through overuse; cliched"),
      ("Impervious", "Unable to be affected by; resistant to"),
      ("Incessant", "Continuing without pause or interruption"),
      ("Innocuous", "Not harmful or offensive"),
      ("Lethargic", "Affected by lethargy; sluggish and apathetic"),
      ("Meticulous", "Showing great attention to detail; very careful"),
      ("Pragmatic", "Dealing with things sensibly and realistically"),
      ("Unprecedented", "Never done or known before"),
    ]
  },
  {
    "slug": "gre-vocabulary",
    "title": "GRE Vocabulary",
    "category": "Test Prep",
    "description": "High-frequency GRE vocabulary words for the verbal reasoning section. Essential for graduate school admissions.",
    "meta_desc": "Free GRE vocabulary flashcards. 50 high-frequency GRE words with definitions. Study online or import into Stacked.",
    "keywords": "GRE vocabulary, GRE vocab flashcards, GRE words, GRE prep, graduate school prep",
    "color": {"hex": "#AF52DE", "r": 0.686, "g": 0.322, "b": 0.969},
    "cards": [
      ("Abate", "To become less intense or widespread"),
      ("Aberrant", "Departing from an accepted standard"),
      ("Abjure", "To formally reject or give up"),
      ("Accolade", "An award or privilege granted as an honor"),
      ("Acrimony", "Bitterness or ill feeling"),
      ("Adulterate", "To make something poorer in quality by adding another substance"),
      ("Alacrity", "Brisk and cheerful readiness"),
      ("Amalgamate", "To combine or unite to form one structure"),
      ("Ambivalent", "Having mixed feelings about something"),
      ("Anachronistic", "Belonging to a period other than the one portrayed"),
      ("Antithetical", "Directly opposed; mutually incompatible"),
      ("Apocryphal", "Of doubtful authenticity, though widely circulated"),
      ("Approbation", "Approval or praise"),
      ("Assuage", "To make an unpleasant feeling less intense"),
      ("Bellicose", "Demonstrating aggression and willingness to fight"),
      ("Calumny", "The making of false statements to damage reputation"),
      ("Capricious", "Given to sudden changes of mood or behavior"),
      ("Chicanery", "The use of trickery to achieve a goal"),
      ("Circumscribe", "To restrict or limit"),
      ("Coalesce", "To come together to form one mass or whole"),
      ("Contrite", "Feeling or expressing remorse"),
      ("Dearth", "A scarcity or lack of something"),
      ("Decorum", "Behavior in keeping with good taste"),
      ("Demur", "To raise doubts or objections"),
      ("Desultory", "Lacking a plan, purpose, or enthusiasm"),
      ("Diatribe", "A forceful and bitter verbal attack"),
      ("Diffident", "Modest or shy because of a lack of self-confidence"),
      ("Disabuse", "To persuade someone that an idea is mistaken"),
      ("Disseminate", "To spread information widely"),
      ("Ebullient", "Cheerful and full of energy"),
      ("Efficacy", "The ability to produce a desired result"),
      ("Enervate", "To drain of energy or vitality"),
      ("Equanimity", "Mental calmness and composure"),
      ("Erudite", "Having or showing great knowledge"),
      ("Excoriate", "To criticize severely"),
      ("Garrulous", "Excessively talkative"),
      ("Iconoclast", "A person who attacks cherished beliefs"),
      ("Implacable", "Unable to be calmed or appeased"),
      ("Inchoate", "Just begun and not fully formed"),
      ("Ingenuous", "Innocent and unsuspecting"),
      ("Laconic", "Using very few words"),
      ("Laud", "To praise highly"),
      ("Magnanimous", "Very generous or forgiving"),
      ("Mendacious", "Not telling the truth; lying"),
      ("Obdurate", "Stubbornly refusing to change"),
      ("Pedantic", "Excessively concerned with minor details"),
      ("Phlegmatic", "Calm and unemotional"),
      ("Probity", "The quality of having strong moral principles"),
      ("Recalcitrant", "Having an obstinately uncooperative attitude"),
      ("Sycophant", "A person who flatters someone important for gain"),
    ]
  },
  {
    "slug": "ap-biology",
    "title": "AP Biology",
    "category": "AP Exams",
    "description": "Key concepts for AP Biology covering cell biology, genetics, evolution, and ecology.",
    "meta_desc": "Free AP Biology flashcards. 50 key concepts covering cells, genetics, evolution, and ecology. Study for the AP Bio exam online.",
    "keywords": "AP Biology flashcards, AP Bio review, AP Biology study cards, AP Bio exam prep",
    "color": {"hex": "#30D158", "r": 0.188, "g": 0.820, "b": 0.345},
    "cards": [
      ("Cell Theory", "All living things are made of cells; cells are the basic unit of life; all cells come from pre-existing cells"),
      ("Mitochondria", "Organelle that produces ATP through cellular respiration; has its own DNA; double membrane structure"),
      ("Chloroplast", "Organelle in plant cells that carries out photosynthesis; contains chlorophyll; has its own DNA"),
      ("DNA Structure", "Double helix of nucleotides; A pairs with T, G pairs with C; sugar-phosphate backbone; antiparallel strands"),
      ("RNA vs DNA", "RNA is single-stranded, uses uracil instead of thymine, has ribose sugar instead of deoxyribose"),
      ("Mitosis", "Cell division producing two identical daughter cells; phases: prophase, metaphase, anaphase, telophase"),
      ("Meiosis", "Cell division producing four haploid gametes; involves crossing over and independent assortment; two rounds of division"),
      ("Photosynthesis Equation", "6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂"),
      ("Cellular Respiration Equation", "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP (36-38 ATP per glucose)"),
      ("Natural Selection", "Organisms with favorable traits are more likely to survive and reproduce; requires variation, heritability, and differential reproduction"),
      ("Hardy-Weinberg Equilibrium", "p² + 2pq + q² = 1; conditions: no mutation, no selection, no migration, random mating, large population"),
      ("Krebs Cycle", "Occurs in mitochondrial matrix; produces 2 ATP, 6 NADH, 2 FADH₂ per glucose; also called citric acid cycle"),
      ("Enzyme Function", "Biological catalysts that lower activation energy; substrate-specific; affected by temperature, pH, and concentration"),
      ("Active Transport", "Movement of molecules against concentration gradient; requires ATP; examples: sodium-potassium pump"),
      ("Passive Transport", "Movement of molecules down concentration gradient; no ATP required; includes diffusion and osmosis"),
      ("Osmosis", "Diffusion of water across a semipermeable membrane from low to high solute concentration"),
      ("Transcription", "DNA → mRNA in the nucleus; RNA polymerase reads template strand 3' to 5'; mRNA is built 5' to 3'"),
      ("Translation", "mRNA → protein at ribosomes; tRNA brings amino acids; codons are read in sets of three nucleotides"),
      ("Dominant vs Recessive", "Dominant allele masks recessive; homozygous dominant (AA), heterozygous (Aa), homozygous recessive (aa)"),
      ("Punnett Square", "Diagram used to predict genotype and phenotype ratios of offspring from a genetic cross"),
      ("Gene Expression", "Process by which DNA information is used to synthesize functional products like proteins"),
      ("Endoplasmic Reticulum", "Rough ER has ribosomes (protein synthesis); Smooth ER lacks ribosomes (lipid synthesis, detoxification)"),
      ("Golgi Apparatus", "Modifies, packages, and ships proteins and lipids; receives from ER; sends vesicles to cell membrane"),
      ("ATP Structure", "Adenosine triphosphate; adenine + ribose + 3 phosphate groups; energy stored in phosphate bonds"),
      ("Ecological Succession", "Primary: starts from bare rock; Secondary: starts from disturbed ecosystem; ends at climax community"),
      ("Food Web", "Interconnected food chains showing energy flow; energy decreases ~90% at each trophic level"),
      ("Symbiosis Types", "Mutualism: both benefit; Commensalism: one benefits, other unaffected; Parasitism: one benefits, other harmed"),
      ("Genetic Drift", "Random changes in allele frequency in small populations; bottleneck effect and founder effect"),
      ("Speciation", "Formation of new species; allopatric (geographic isolation) vs sympatric (same location, reproductive isolation)"),
      ("Homeostasis", "Maintenance of stable internal conditions; uses negative feedback loops; examples: body temperature, blood glucose"),
      ("Water Properties", "Cohesion, adhesion, high specific heat, universal solvent, density anomaly (ice floats)"),
      ("pH Scale", "Measures hydrogen ion concentration; 0-14 scale; 7 is neutral; below 7 acidic; above 7 basic"),
      ("Lipids", "Fats, oils, waxes; hydrophobic; made of glycerol + fatty acids; energy storage and cell membranes"),
      ("Proteins", "Made of amino acids; 20 types; peptide bonds; 4 structural levels: primary, secondary, tertiary, quaternary"),
      ("Carbohydrates", "Sugars and starches; monosaccharides, disaccharides, polysaccharides; quick energy source; C:H:O ratio 1:2:1"),
      ("Nucleic Acids", "DNA and RNA; made of nucleotides; store and transmit genetic information"),
      ("Cell Membrane Structure", "Phospholipid bilayer with embedded proteins; fluid mosaic model; selectively permeable"),
      ("Immune System", "Innate (non-specific) and adaptive (specific) immunity; B cells make antibodies; T cells kill infected cells"),
      ("Nervous System", "Neurons transmit electrical signals; synapse uses neurotransmitters; central (brain/spinal cord) and peripheral"),
      ("Endocrine System", "Hormone-based signaling; slower than nervous system; pituitary is master gland; uses feedback loops"),
    ]
  },
  {
    "slug": "ap-us-history",
    "title": "AP US History (APUSH)",
    "category": "AP Exams",
    "description": "Key events, people, and concepts for AP US History from colonization to modern America.",
    "meta_desc": "Free APUSH flashcards. Key events, people, and concepts from colonization to modern America. Study for the AP US History exam.",
    "keywords": "APUSH flashcards, AP US History study cards, APUSH review, AP History exam prep",
    "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
    "cards": [
      ("Jamestown (1607)", "First permanent English settlement in North America; Virginia; funded by Virginia Company; John Smith"),
      ("Mayflower Compact (1620)", "First governing document of Plymouth Colony; established self-governance; signed by Pilgrims"),
      ("Great Awakening (1730s-1740s)", "Religious revival movement; Jonathan Edwards, George Whitefield; challenged established churches; promoted individualism"),
      ("French and Indian War (1754-1763)", "Britain vs France for North American territory; British won; led to taxes on colonies; Treaty of Paris 1763"),
      ("Stamp Act (1765)", "British tax on paper goods in colonies; 'No taxation without representation'; repealed 1766 after protests"),
      ("Declaration of Independence (1776)", "Written by Thomas Jefferson; declared independence from Britain; based on natural rights philosophy; July 4"),
      ("Articles of Confederation", "First US constitution (1781-1789); weak central government; no power to tax; replaced by Constitution"),
      ("Constitutional Convention (1787)", "Philadelphia; created US Constitution; Great Compromise (bicameral legislature); Three-Fifths Compromise"),
      ("Bill of Rights (1791)", "First 10 amendments to Constitution; protects individual liberties; James Madison primary author"),
      ("Louisiana Purchase (1803)", "US bought territory from France for $15 million; doubled US size; Lewis and Clark expedition followed"),
      ("War of 1812", "US vs Britain; impressment of sailors; Battle of New Orleans; Treaty of Ghent; boosted American nationalism"),
      ("Monroe Doctrine (1823)", "US policy opposing European colonization in the Americas; 'America for Americans'; shaped foreign policy"),
      ("Manifest Destiny", "Belief that US expansion across North America was justified and inevitable; drove westward expansion"),
      ("Missouri Compromise (1820)", "Admitted Missouri as slave state, Maine as free state; prohibited slavery above 36°30' line"),
      ("Civil War (1861-1865)", "North (Union) vs South (Confederacy); slavery, states' rights; Union won; 620,000+ died"),
      ("Emancipation Proclamation (1863)", "Lincoln freed slaves in Confederate states; shifted war goal to include ending slavery"),
      ("Reconstruction (1865-1877)", "Rebuilding the South after Civil War; 13th, 14th, 15th Amendments; ended with Compromise of 1877"),
      ("13th Amendment (1865)", "Abolished slavery in the United States"),
      ("14th Amendment (1868)", "Granted citizenship to all persons born in US; equal protection under the law; due process"),
      ("15th Amendment (1870)", "Prohibited denying the right to vote based on race, color, or previous condition of servitude"),
      ("Gilded Age (1870s-1900)", "Rapid industrialization; wealth inequality; Carnegie, Rockefeller, Vanderbilt; labor unions formed"),
      ("Progressive Era (1890s-1920s)", "Social reform movement; trust-busting; women's suffrage; food/drug regulation; muckrakers"),
      ("Spanish-American War (1898)", "US vs Spain; 'Remember the Maine'; US gained Philippines, Guam, Puerto Rico; became world power"),
      ("World War I (1914-1918)", "US entered 1917; Treaty of Versailles; League of Nations; Wilson's 14 Points; isolationism after"),
      ("Great Depression (1929-1939)", "Stock market crash; 25% unemployment; Dust Bowl; bank failures; global economic crisis"),
      ("New Deal", "FDR's programs to combat Great Depression; Social Security, FDIC, WPA; expanded federal government role"),
      ("World War II (1939-1945)", "US entered after Pearl Harbor (1941); D-Day 1944; atomic bombs on Japan 1945; Allied victory"),
      ("Cold War (1947-1991)", "US vs Soviet Union ideological conflict; nuclear arms race; proxy wars; containment policy; ended with USSR collapse"),
      ("Brown v Board of Education (1954)", "Supreme Court ruled school segregation unconstitutional; overturned Plessy v Ferguson; civil rights milestone"),
      ("Civil Rights Act (1964)", "Outlawed discrimination based on race, color, religion, sex, or national origin; LBJ signed"),
    ]
  },
  {
    "slug": "ap-psychology",
    "title": "AP Psychology",
    "category": "AP Exams",
    "description": "Key terms, theories, and psychologists for AP Psychology covering all major units.",
    "meta_desc": "Free AP Psychology flashcards. Key terms, theories, and psychologists. Study for the AP Psych exam online or import into Stacked.",
    "keywords": "AP Psychology flashcards, AP Psych review, AP Psychology study cards, psychology exam prep",
    "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
    "cards": [
      ("Classical Conditioning", "Learning through association; Pavlov's dogs; neutral stimulus becomes conditioned stimulus after pairing with unconditioned stimulus"),
      ("Operant Conditioning", "Learning through consequences; B.F. Skinner; reinforcement increases behavior, punishment decreases behavior"),
      ("Maslow's Hierarchy of Needs", "Physiological → Safety → Love/Belonging → Esteem → Self-Actualization; must meet lower needs first"),
      ("Cognitive Dissonance", "Leon Festinger; mental discomfort from holding contradictory beliefs; people change attitudes to reduce discomfort"),
      ("Stanford Prison Experiment", "Philip Zimbardo (1971); students assigned guard/prisoner roles; showed power of situational forces on behavior"),
      ("Milgram Obedience Study", "Stanley Milgram (1963); participants administered fake shocks; 65% obeyed authority to maximum voltage level"),
      ("Nature vs Nurture", "Debate over whether behavior is determined by genetics (nature) or environment/experience (nurture); most traits are both"),
      ("Id, Ego, Superego", "Freud's personality theory; Id: pleasure principle; Ego: reality principle; Superego: moral conscience"),
      ("Stages of Sleep", "Stage 1-3 (NREM, progressively deeper) → REM (dreaming, brain active); cycles ~90 minutes"),
      ("REM Sleep", "Rapid Eye Movement; vivid dreaming occurs; brain is active; body is paralyzed; important for memory consolidation"),
      ("Short-term Memory", "Limited capacity (7±2 items); lasts ~20-30 seconds without rehearsal; working memory model by Baddeley"),
      ("Long-term Memory", "Unlimited capacity and duration; explicit (declarative) and implicit (procedural); requires encoding and consolidation"),
      ("Bystander Effect", "People less likely to help when others are present; diffusion of responsibility; Kitty Genovese case"),
      ("Confirmation Bias", "Tendency to search for information that confirms existing beliefs; ignore contradictory evidence"),
      ("Heuristics", "Mental shortcuts for quick decisions; availability heuristic (ease of recall); representativeness heuristic (stereotypes)"),
      ("Fundamental Attribution Error", "Tendency to attribute others' behavior to personality rather than situational factors"),
      ("Piaget's Stages", "Sensorimotor (0-2) → Preoperational (2-7) → Concrete operational (7-11) → Formal operational (11+)"),
      ("Erikson's Psychosocial Stages", "8 stages of development from birth to death; each has a crisis: Trust vs Mistrust, Identity vs Role Confusion, etc."),
      ("Attachment Theory", "Bowlby/Ainsworth; secure, anxious-avoidant, anxious-resistant attachment styles; formed in infancy; affects adult relationships"),
      ("Fight or Flight Response", "Sympathetic nervous system activation in response to perceived threat; adrenaline release; increased heart rate"),
      ("Neurotransmitters", "Chemical messengers: Serotonin (mood), Dopamine (reward), GABA (inhibition), Acetylcholine (memory), Norepinephrine (arousal)"),
      ("Broca's Area", "Left frontal lobe; controls speech production; damage causes Broca's aphasia (can understand but can't speak fluently)"),
      ("Wernicke's Area", "Left temporal lobe; controls language comprehension; damage causes fluent but nonsensical speech"),
      ("Longitudinal Study", "Same participants studied over a long period; tracks changes over time; expensive and time-consuming"),
      ("Correlation vs Causation", "Correlation shows relationship between variables but does NOT prove one causes the other"),
      ("Placebo Effect", "Improvement in condition due to belief in treatment rather than the treatment itself"),
      ("DSM-5", "Diagnostic and Statistical Manual of Mental Disorders; standard classification of mental disorders; used by clinicians"),
      ("Schizophrenia", "Psychotic disorder; positive symptoms (hallucinations, delusions) and negative symptoms (flat affect, social withdrawal)"),
      ("Major Depressive Disorder", "Persistent sadness, loss of interest, sleep/appetite changes; linked to low serotonin; treated with SSRIs and therapy"),
      ("Big Five Personality Traits", "OCEAN: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism"),
    ]
  },
  {
    "slug": "spanish-101",
    "title": "Spanish 101 — Common Phrases",
    "category": "Languages",
    "description": "Essential Spanish phrases and vocabulary for beginners. Perfect for Spanish 1 students or travelers.",
    "meta_desc": "Free Spanish flashcards for beginners. 50 essential phrases and vocabulary words. Study online or import into Stacked.",
    "keywords": "Spanish flashcards, learn Spanish, Spanish vocabulary, Spanish 101, basic Spanish phrases",
    "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
    "cards": [
      ("Hello", "Hola"),
      ("Goodbye", "Adiós"),
      ("Please", "Por favor"),
      ("Thank you", "Gracias"),
      ("You're welcome", "De nada"),
      ("Good morning", "Buenos días"),
      ("Good afternoon", "Buenas tardes"),
      ("Good night", "Buenas noches"),
      ("How are you?", "¿Cómo estás?"),
      ("I'm fine, thanks", "Estoy bien, gracias"),
      ("What is your name?", "¿Cómo te llamas?"),
      ("My name is...", "Me llamo..."),
      ("Nice to meet you", "Mucho gusto"),
      ("Yes", "Sí"),
      ("No", "No"),
      ("Excuse me", "Perdón / Disculpe"),
      ("I'm sorry", "Lo siento"),
      ("I don't understand", "No entiendo"),
      ("Do you speak English?", "¿Hablas inglés?"),
      ("Where is...?", "¿Dónde está...?"),
      ("How much does it cost?", "¿Cuánto cuesta?"),
      ("Water", "Agua"),
      ("Food", "Comida"),
      ("Bathroom", "Baño"),
      ("Help!", "¡Ayuda!"),
      ("I need", "Necesito"),
      ("I want", "Quiero"),
      ("I like", "Me gusta"),
      ("Today", "Hoy"),
      ("Tomorrow", "Mañana"),
      ("Yesterday", "Ayer"),
      ("One", "Uno"),
      ("Two", "Dos"),
      ("Three", "Tres"),
      ("Four", "Cuatro"),
      ("Five", "Cinco"),
      ("Monday", "Lunes"),
      ("Tuesday", "Martes"),
      ("Wednesday", "Miércoles"),
      ("Thursday", "Jueves"),
      ("Friday", "Viernes"),
      ("Family", "Familia"),
      ("Friend", "Amigo / Amiga"),
      ("House", "Casa"),
      ("School", "Escuela"),
      ("Work", "Trabajo"),
      ("To eat", "Comer"),
      ("To drink", "Beber"),
      ("To go", "Ir"),
      ("To be (permanent)", "Ser"),
    ]
  },
  {
    "slug": "french-101",
    "title": "French 101 — Common Phrases",
    "category": "Languages",
    "description": "Essential French phrases and vocabulary for beginners. Perfect for French 1 students or travelers visiting France.",
    "meta_desc": "Free French flashcards for beginners. 40 essential phrases and vocabulary words. Study online or import into Stacked.",
    "keywords": "French flashcards, learn French, French vocabulary, French 101, basic French phrases",
    "color": {"hex": "#007AFF", "r": 0.0, "g": 0.478, "b": 1.0},
    "cards": [
      ("Hello", "Bonjour"),
      ("Goodbye", "Au revoir"),
      ("Please", "S'il vous plaît"),
      ("Thank you", "Merci"),
      ("You're welcome", "De rien"),
      ("Good evening", "Bonsoir"),
      ("How are you?", "Comment allez-vous?"),
      ("I'm fine", "Je vais bien"),
      ("What is your name?", "Comment vous appelez-vous?"),
      ("My name is...", "Je m'appelle..."),
      ("Yes", "Oui"),
      ("No", "Non"),
      ("Excuse me", "Excusez-moi"),
      ("I'm sorry", "Je suis désolé(e)"),
      ("I don't understand", "Je ne comprends pas"),
      ("Do you speak English?", "Parlez-vous anglais?"),
      ("Where is...?", "Où est...?"),
      ("How much?", "Combien?"),
      ("Water", "L'eau"),
      ("Bread", "Le pain"),
      ("I would like", "Je voudrais"),
      ("Today", "Aujourd'hui"),
      ("Tomorrow", "Demain"),
      ("One", "Un/Une"),
      ("Two", "Deux"),
      ("Three", "Trois"),
      ("Four", "Quatre"),
      ("Five", "Cinq"),
      ("Monday", "Lundi"),
      ("Tuesday", "Mardi"),
      ("Wednesday", "Mercredi"),
      ("The restaurant", "Le restaurant"),
      ("The hotel", "L'hôtel"),
      ("The train station", "La gare"),
      ("To eat", "Manger"),
      ("To drink", "Boire"),
      ("To go", "Aller"),
      ("To be", "Être"),
      ("To have", "Avoir"),
      ("I love", "J'aime"),
    ]
  },
  {
    "slug": "japanese-hiragana",
    "title": "Japanese Hiragana",
    "category": "Languages",
    "description": "Learn all 46 basic Hiragana characters. The essential first step to reading Japanese.",
    "meta_desc": "Free Japanese Hiragana flashcards. All 46 basic characters with romaji pronunciation. Study online or import into Stacked.",
    "keywords": "Hiragana flashcards, learn Hiragana, Japanese alphabet, Japanese flashcards, learn Japanese",
    "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
    "cards": [
      ("あ", "a"), ("い", "i"), ("う", "u"), ("え", "e"), ("お", "o"),
      ("か", "ka"), ("き", "ki"), ("く", "ku"), ("け", "ke"), ("こ", "ko"),
      ("さ", "sa"), ("し", "shi"), ("す", "su"), ("せ", "se"), ("そ", "so"),
      ("た", "ta"), ("ち", "chi"), ("つ", "tsu"), ("て", "te"), ("と", "to"),
      ("な", "na"), ("に", "ni"), ("ぬ", "nu"), ("ね", "ne"), ("の", "no"),
      ("は", "ha"), ("ひ", "hi"), ("ふ", "fu"), ("へ", "he"), ("ほ", "ho"),
      ("ま", "ma"), ("み", "mi"), ("む", "mu"), ("め", "me"), ("も", "mo"),
      ("や", "ya"), ("ゆ", "yu"), ("よ", "yo"),
      ("ら", "ra"), ("り", "ri"), ("る", "ru"), ("れ", "re"), ("ろ", "ro"),
      ("わ", "wa"), ("を", "wo"), ("ん", "n"),
    ]
  },
  {
    "slug": "anatomy-physiology",
    "title": "Anatomy & Physiology",
    "category": "College",
    "description": "Essential anatomy and physiology terms covering body systems, organs, and functions.",
    "meta_desc": "Free Anatomy & Physiology flashcards. Key terms for body systems, organs, and functions. Study online or import into Stacked.",
    "keywords": "anatomy flashcards, physiology flashcards, anatomy and physiology, A&P study cards, human body systems",
    "color": {"hex": "#30D158", "r": 0.188, "g": 0.820, "b": 0.345},
    "cards": [
      ("Skeletal System", "206 bones in adults; provides support, protection, movement, blood cell production, and mineral storage"),
      ("Muscular System", "3 types: skeletal (voluntary), smooth (involuntary), cardiac (heart); enables movement and posture"),
      ("Nervous System", "Brain, spinal cord, nerves; CNS (central) and PNS (peripheral); transmits electrical signals"),
      ("Cardiovascular System", "Heart, blood vessels, blood; pumps ~2,000 gallons of blood per day; delivers O₂ and nutrients"),
      ("Respiratory System", "Lungs, trachea, bronchi; gas exchange: O₂ in, CO₂ out; diaphragm controls breathing"),
      ("Digestive System", "Mouth → esophagus → stomach → small intestine → large intestine; breaks down food for absorption"),
      ("Endocrine System", "Hormone-producing glands; pituitary, thyroid, adrenal, pancreas; regulates metabolism, growth, mood"),
      ("Lymphatic System", "Lymph nodes, spleen, thymus; filters pathogens; returns fluid to bloodstream; immune function"),
      ("Urinary System", "Kidneys, ureters, bladder, urethra; filters blood; removes waste as urine; regulates fluid balance"),
      ("Integumentary System", "Skin, hair, nails; largest organ; protects against infection, UV, dehydration; temperature regulation"),
      ("Femur", "Longest and strongest bone in the body; located in the thigh; connects hip to knee"),
      ("Humerus", "Upper arm bone; connects shoulder to elbow; articulates with scapula and radius/ulna"),
      ("Cranium", "Skull bones protecting the brain; 8 cranial bones fused together; frontal, parietal, temporal, occipital"),
      ("Vertebral Column", "33 vertebrae: 7 cervical, 12 thoracic, 5 lumbar, 5 sacral (fused), 4 coccygeal (fused)"),
      ("Heart Chambers", "4 chambers: right atrium, right ventricle, left atrium, left ventricle; left side pumps to body"),
      ("Blood Types", "A, B, AB, O; determined by antigens on red blood cells; Rh factor (+ or -); O- is universal donor"),
      ("Red Blood Cells", "Erythrocytes; carry oxygen via hemoglobin; no nucleus; produced in bone marrow; live ~120 days"),
      ("White Blood Cells", "Leukocytes; fight infection; types include neutrophils, lymphocytes, monocytes; part of immune system"),
      ("Neurons", "Nerve cells; dendrites receive signals, axon transmits signals; synapse connects neurons; myelin speeds transmission"),
      ("Cerebrum", "Largest part of brain; 4 lobes; responsible for thinking, memory, language, voluntary movement"),
      ("Cerebellum", "Located at back of brain; coordinates movement, balance, posture; 'little brain'"),
      ("Alveoli", "Tiny air sacs in lungs; site of gas exchange; surrounded by capillaries; ~300 million per lung"),
      ("Diaphragm", "Dome-shaped muscle below lungs; contracts to expand chest cavity during inhalation"),
      ("Liver", "Largest internal organ; detoxifies blood, produces bile, stores glycogen, synthesizes proteins"),
      ("Kidneys", "Filter ~200 liters of blood daily; produce urine; regulate electrolytes, pH, and blood pressure"),
      ("Pancreas", "Dual function: endocrine (insulin, glucagon) and exocrine (digestive enzymes); regulates blood sugar"),
      ("Thyroid Gland", "Butterfly-shaped gland in neck; produces T3 and T4; regulates metabolism, growth, and development"),
      ("Adrenal Glands", "Located on top of kidneys; produce cortisol (stress), aldosterone (blood pressure), adrenaline (fight/flight)"),
      ("Tendons", "Connect muscle to bone; made of dense connective tissue; transmit force from muscle contraction"),
      ("Ligaments", "Connect bone to bone; stabilize joints; made of collagen fibers; can be stretched or torn"),
    ]
  },
  {
    "slug": "us-state-capitals",
    "title": "US State Capitals",
    "category": "General Knowledge",
    "description": "All 50 US state capitals. A must-know for geography, civics, and general knowledge.",
    "meta_desc": "Free US State Capitals flashcards. All 50 states and their capitals. Study online or import into Stacked.",
    "keywords": "US state capitals flashcards, state capitals quiz, 50 states capitals, geography flashcards",
    "color": {"hex": "#007AFF", "r": 0.0, "g": 0.478, "b": 1.0},
    "cards": [
      ("Alabama", "Montgomery"), ("Alaska", "Juneau"), ("Arizona", "Phoenix"), ("Arkansas", "Little Rock"),
      ("California", "Sacramento"), ("Colorado", "Denver"), ("Connecticut", "Hartford"), ("Delaware", "Dover"),
      ("Florida", "Tallahassee"), ("Georgia", "Atlanta"), ("Hawaii", "Honolulu"), ("Idaho", "Boise"),
      ("Illinois", "Springfield"), ("Indiana", "Indianapolis"), ("Iowa", "Des Moines"), ("Kansas", "Topeka"),
      ("Kentucky", "Frankfort"), ("Louisiana", "Baton Rouge"), ("Maine", "Augusta"), ("Maryland", "Annapolis"),
      ("Massachusetts", "Boston"), ("Michigan", "Lansing"), ("Minnesota", "Saint Paul"), ("Mississippi", "Jackson"),
      ("Missouri", "Jefferson City"), ("Montana", "Helena"), ("Nebraska", "Lincoln"), ("Nevada", "Carson City"),
      ("New Hampshire", "Concord"), ("New Jersey", "Trenton"), ("New Mexico", "Santa Fe"), ("New York", "Albany"),
      ("North Carolina", "Raleigh"), ("North Dakota", "Bismarck"), ("Ohio", "Columbus"), ("Oklahoma", "Oklahoma City"),
      ("Oregon", "Salem"), ("Pennsylvania", "Harrisburg"), ("Rhode Island", "Providence"), ("South Carolina", "Columbia"),
      ("South Dakota", "Pierre"), ("Tennessee", "Nashville"), ("Texas", "Austin"), ("Utah", "Salt Lake City"),
      ("Vermont", "Montpelier"), ("Virginia", "Richmond"), ("Washington", "Olympia"), ("West Virginia", "Charleston"),
      ("Wisconsin", "Madison"), ("Wyoming", "Cheyenne"),
    ]
  },
  {
    "slug": "periodic-table",
    "title": "Periodic Table — First 30 Elements",
    "category": "Science",
    "description": "The first 30 elements of the periodic table with symbols and atomic numbers.",
    "meta_desc": "Free Periodic Table flashcards. First 30 elements with symbols and atomic numbers. Study chemistry online or import into Stacked.",
    "keywords": "periodic table flashcards, elements flashcards, chemistry flashcards, periodic table study",
    "color": {"hex": "#5AC8FA", "r": 0.353, "g": 0.784, "b": 0.980},
    "cards": [
      ("1 - Hydrogen", "H — Lightest element; most abundant in universe; gas"),
      ("2 - Helium", "He — Noble gas; second lightest; used in balloons"),
      ("3 - Lithium", "Li — Alkali metal; lightest metal; used in batteries"),
      ("4 - Beryllium", "Be — Alkaline earth metal; lightweight; toxic"),
      ("5 - Boron", "B — Metalloid; used in glass and detergents"),
      ("6 - Carbon", "C — Basis of organic chemistry; found in all living things"),
      ("7 - Nitrogen", "N — Makes up 78% of atmosphere; essential for life"),
      ("8 - Oxygen", "O — Makes up 21% of atmosphere; essential for respiration"),
      ("9 - Fluorine", "F — Most reactive element; halogen; used in toothpaste"),
      ("10 - Neon", "Ne — Noble gas; used in neon signs; orange-red glow"),
      ("11 - Sodium", "Na — Alkali metal; highly reactive; component of table salt (NaCl)"),
      ("12 - Magnesium", "Mg — Alkaline earth metal; lightweight; essential mineral for humans"),
      ("13 - Aluminum", "Al — Most abundant metal in Earth's crust; lightweight"),
      ("14 - Silicon", "Si — Metalloid; used in computer chips and glass"),
      ("15 - Phosphorus", "P — Essential for DNA and ATP; found in bones and teeth"),
      ("16 - Sulfur", "S — Yellow solid; 'rotten egg' smell; used in fertilizers"),
      ("17 - Chlorine", "Cl — Halogen; used in water purification; part of table salt"),
      ("18 - Argon", "Ar — Noble gas; third most abundant gas in atmosphere"),
      ("19 - Potassium", "K — Alkali metal; essential nutrient; found in bananas"),
      ("20 - Calcium", "Ca — Alkaline earth metal; essential for bones and teeth"),
      ("21 - Scandium", "Sc — Transition metal; lightweight; used in aerospace alloys"),
      ("22 - Titanium", "Ti — Transition metal; strong, lightweight, corrosion-resistant"),
      ("23 - Vanadium", "V — Transition metal; used in steel alloys"),
      ("24 - Chromium", "Cr — Transition metal; used in stainless steel; chrome plating"),
      ("25 - Manganese", "Mn — Transition metal; essential trace element; used in steel"),
      ("26 - Iron", "Fe — Most used metal; essential for hemoglobin; magnetic"),
      ("27 - Cobalt", "Co — Transition metal; used in magnets and batteries; blue pigment"),
      ("28 - Nickel", "Ni — Transition metal; corrosion-resistant; used in coins and alloys"),
      ("29 - Copper", "Cu — Excellent conductor; used in wiring and plumbing; reddish color"),
      ("30 - Zinc", "Zn — Transition metal; used in galvanizing steel; essential mineral"),
    ]
  },
  {
    "slug": "psychology-101",
    "title": "Psychology 101",
    "category": "College",
    "description": "Introductory psychology concepts covering major theories, disorders, and researchers.",
    "meta_desc": "Free Psychology 101 flashcards. Key concepts, theories, and researchers for intro psych. Study online or import into Stacked.",
    "keywords": "psychology 101 flashcards, intro psych, psychology study cards, psych 101 terms",
    "color": {"hex": "#AF52DE", "r": 0.686, "g": 0.322, "b": 0.969},
    "cards": [
      ("Psychology", "The scientific study of behavior and mental processes"),
      ("Behaviorism", "School of thought focusing on observable behavior; Watson, Skinner; environment shapes behavior"),
      ("Psychoanalysis", "Freud's theory; unconscious drives behavior; id, ego, superego; dream analysis; free association"),
      ("Humanistic Psychology", "Maslow, Rogers; focuses on personal growth and self-actualization; positive view of human nature"),
      ("Cognitive Psychology", "Study of mental processes: thinking, memory, perception, problem-solving, language"),
      ("Biological Psychology", "Studies how brain, neurotransmitters, and genetics influence behavior"),
      ("Developmental Psychology", "Study of how people change across the lifespan; cognitive, social, and physical development"),
      ("Social Psychology", "How people think about, influence, and relate to one another; conformity, obedience, group dynamics"),
      ("Clinical Psychology", "Assessment, diagnosis, and treatment of mental disorders"),
      ("Independent Variable", "The variable that is manipulated in an experiment; the cause"),
      ("Dependent Variable", "The variable that is measured in an experiment; the effect"),
      ("Control Group", "Group that does not receive the treatment; used for comparison"),
      ("Random Assignment", "Each participant has equal chance of being in any group; reduces bias"),
      ("Reliability", "Consistency of a measure; test gives same results each time"),
      ("Validity", "Does the test measure what it claims to measure?"),
      ("Positive Reinforcement", "Adding a pleasant stimulus to increase behavior (e.g., giving a treat for good behavior)"),
      ("Negative Reinforcement", "Removing an unpleasant stimulus to increase behavior (e.g., stopping an alarm when you wake up)"),
      ("Positive Punishment", "Adding an unpleasant stimulus to decrease behavior (e.g., getting a speeding ticket)"),
      ("Negative Punishment", "Removing a pleasant stimulus to decrease behavior (e.g., taking away phone privileges)"),
      ("Observational Learning", "Learning by watching others; Bandura's Bobo doll experiment; modeling"),
      ("Selective Attention", "Focusing on one stimulus while ignoring others; cocktail party effect"),
      ("Conformity", "Adjusting behavior to match group norms; Asch's line experiment"),
      ("Groupthink", "Poor decisions made by groups seeking consensus; suppresses dissent"),
      ("Obedience", "Following orders from authority; Milgram's shock experiment"),
      ("Attribution Theory", "How we explain others' behavior; internal (dispositional) vs external (situational) attributions"),
      ("Anxiety Disorders", "Excessive worry/fear; includes GAD, panic disorder, phobias, social anxiety, OCD"),
      ("Defense Mechanisms", "Freud; unconscious strategies to reduce anxiety: repression, denial, projection, rationalization"),
      ("Stages of Grief", "Kübler-Ross: Denial → Anger → Bargaining → Depression → Acceptance"),
      ("Neuroplasticity", "Brain's ability to reorganize and form new neural connections throughout life"),
      ("Circadian Rhythm", "24-hour biological clock; regulates sleep-wake cycle; influenced by light exposure"),
    ]
  },
  {
    "slug": "medical-terminology",
    "title": "Medical Terminology",
    "category": "Professional",
    "description": "Essential medical prefixes, suffixes, and terms for healthcare students and professionals.",
    "meta_desc": "Free medical terminology flashcards. Essential prefixes, suffixes, and terms for healthcare students. Study online or import into Stacked.",
    "keywords": "medical terminology flashcards, medical terms study cards, healthcare vocabulary, nursing flashcards",
    "color": {"hex": "#30D158", "r": 0.188, "g": 0.820, "b": 0.345},
    "cards": [
      ("-itis", "Inflammation (e.g., arthritis = joint inflammation)"),
      ("-ectomy", "Surgical removal (e.g., appendectomy = removal of appendix)"),
      ("-ology", "Study of (e.g., cardiology = study of the heart)"),
      ("-osis", "Abnormal condition (e.g., cyanosis = blue discoloration)"),
      ("-pathy", "Disease or suffering (e.g., neuropathy = nerve disease)"),
      ("-scopy", "Visual examination (e.g., endoscopy = examining inside the body)"),
      ("-plasty", "Surgical repair (e.g., rhinoplasty = nose repair/reshaping)"),
      ("-algia", "Pain (e.g., neuralgia = nerve pain)"),
      ("Cardio-", "Heart (e.g., cardiovascular = relating to heart and blood vessels)"),
      ("Neuro-", "Nerve/nervous system (e.g., neurology = study of nervous system)"),
      ("Derm-/Derma-", "Skin (e.g., dermatology = study of skin)"),
      ("Hemo-/Hemato-", "Blood (e.g., hematology = study of blood)"),
      ("Hepato-", "Liver (e.g., hepatitis = liver inflammation)"),
      ("Nephro-/Reno-", "Kidney (e.g., nephrology = study of kidneys)"),
      ("Osteo-", "Bone (e.g., osteoporosis = porous/weak bones)"),
      ("Pulmo-", "Lung (e.g., pulmonology = study of lungs)"),
      ("Gastro-", "Stomach (e.g., gastritis = stomach inflammation)"),
      ("Hyper-", "Above normal/excessive (e.g., hypertension = high blood pressure)"),
      ("Hypo-", "Below normal/deficient (e.g., hypoglycemia = low blood sugar)"),
      ("Tachy-", "Fast (e.g., tachycardia = fast heart rate, >100 bpm)"),
      ("Brady-", "Slow (e.g., bradycardia = slow heart rate, <60 bpm)"),
      ("Anti-", "Against (e.g., antibiotic = against bacteria)"),
      ("Dys-", "Difficult/painful/abnormal (e.g., dyspnea = difficulty breathing)"),
      ("Anterior", "Front of the body"),
      ("Posterior", "Back of the body"),
      ("Superior", "Above; toward the head"),
      ("Inferior", "Below; toward the feet"),
      ("Lateral", "Away from the midline; toward the side"),
      ("Medial", "Toward the midline; toward the center"),
      ("Vital Signs", "Temperature, pulse, respiration rate, blood pressure; basic health indicators"),
    ]
  },
  {
    "slug": "world-capitals",
    "title": "World Capitals",
    "category": "General Knowledge",
    "description": "Capital cities of 40 major countries around the world.",
    "meta_desc": "Free World Capitals flashcards. 40 major countries and their capitals. Study geography online or import into Stacked.",
    "keywords": "world capitals flashcards, country capitals, geography flashcards, capitals quiz",
    "color": {"hex": "#5AC8FA", "r": 0.353, "g": 0.784, "b": 0.980},
    "cards": [
      ("United Kingdom", "London"), ("France", "Paris"), ("Germany", "Berlin"), ("Spain", "Madrid"),
      ("Italy", "Rome"), ("Japan", "Tokyo"), ("China", "Beijing"), ("India", "New Delhi"),
      ("Russia", "Moscow"), ("Brazil", "Brasília"), ("Australia", "Canberra"), ("Canada", "Ottawa"),
      ("Mexico", "Mexico City"), ("South Korea", "Seoul"), ("Egypt", "Cairo"), ("Turkey", "Ankara"),
      ("Argentina", "Buenos Aires"), ("South Africa", "Pretoria"), ("Thailand", "Bangkok"), ("Vietnam", "Hanoi"),
      ("Nigeria", "Abuja"), ("Kenya", "Nairobi"), ("Sweden", "Stockholm"), ("Norway", "Oslo"),
      ("Denmark", "Copenhagen"), ("Poland", "Warsaw"), ("Netherlands", "Amsterdam"), ("Belgium", "Brussels"),
      ("Switzerland", "Bern"), ("Austria", "Vienna"), ("Greece", "Athens"), ("Portugal", "Lisbon"),
      ("Ireland", "Dublin"), ("Czech Republic", "Prague"), ("Israel", "Jerusalem"), ("Saudi Arabia", "Riyadh"),
      ("Indonesia", "Jakarta"), ("Philippines", "Manila"), ("Colombia", "Bogotá"), ("Peru", "Lima"),
    ]
  },
  {
    "slug": "literary-terms",
    "title": "Literary Terms",
    "category": "English",
    "description": "Key literary terms and devices for English class, AP Literature, and the SAT reading section.",
    "meta_desc": "Free literary terms flashcards. Key literary devices for English class and AP Lit. Study online or import into Stacked.",
    "keywords": "literary terms flashcards, literary devices, AP Literature, English class study cards",
    "color": {"hex": "#AF52DE", "r": 0.686, "g": 0.322, "b": 0.969},
    "cards": [
      ("Metaphor", "A comparison between two unlike things WITHOUT using 'like' or 'as' (e.g., 'Time is money')"),
      ("Simile", "A comparison between two unlike things USING 'like' or 'as' (e.g., 'Brave as a lion')"),
      ("Personification", "Giving human qualities to non-human things (e.g., 'The wind whispered')"),
      ("Hyperbole", "Extreme exaggeration for emphasis (e.g., 'I've told you a million times')"),
      ("Alliteration", "Repetition of the same consonant sound at the beginning of words (e.g., 'Peter Piper picked')"),
      ("Onomatopoeia", "Words that imitate sounds (e.g., 'buzz', 'hiss', 'crash', 'sizzle')"),
      ("Irony", "When the opposite of what is expected occurs; types: verbal, situational, dramatic"),
      ("Foreshadowing", "Hints or clues about events that will happen later in the story"),
      ("Symbolism", "Using an object to represent a larger idea (e.g., dove = peace, darkness = evil)"),
      ("Allegory", "A narrative where characters and events represent abstract ideas or moral lessons (e.g., Animal Farm)"),
      ("Imagery", "Descriptive language that appeals to the five senses (sight, sound, smell, taste, touch)"),
      ("Tone", "The author's attitude toward the subject (e.g., sarcastic, nostalgic, hopeful)"),
      ("Mood", "The emotional atmosphere a text creates for the reader (e.g., suspenseful, gloomy, cheerful)"),
      ("Theme", "The central message or underlying meaning of a literary work"),
      ("Protagonist", "The main character of a story; drives the plot forward"),
      ("Antagonist", "The character or force that opposes the protagonist"),
      ("Conflict", "The central struggle; types: person vs person, person vs nature, person vs self, person vs society"),
      ("Climax", "The turning point or moment of highest tension in the plot"),
      ("Allusion", "A reference to another literary work, person, or event (e.g., 'He was a real Romeo')"),
      ("Paradox", "A statement that seems contradictory but reveals a truth (e.g., 'Less is more')"),
      ("Oxymoron", "Two contradictory words placed together (e.g., 'deafening silence', 'bittersweet')"),
      ("Juxtaposition", "Placing two contrasting elements side by side for comparison or emphasis"),
      ("Satire", "Using humor, irony, or exaggeration to criticize or mock people, institutions, or society"),
      ("Point of View", "Perspective from which a story is told: first person (I), second person (you), third person (he/she)"),
      ("Flashback", "A scene set in a time earlier than the main story; provides background information"),
      ("Motif", "A recurring element (image, symbol, theme) that supports the main theme"),
      ("Diction", "The author's choice of words; can be formal, informal, technical, etc."),
      ("Syntax", "The arrangement of words and phrases to create sentences; affects rhythm and emphasis"),
      ("Rhetoric", "The art of persuasion; appeals: ethos (credibility), pathos (emotion), logos (logic)"),
      ("Soliloquy", "A speech in a play where a character speaks their thoughts aloud, alone on stage"),
    ]
  },
  {
    "slug": "economics-101",
    "title": "Economics 101",
    "category": "College",
    "description": "Fundamental economics concepts including supply and demand, market structures, and macroeconomic indicators.",
    "meta_desc": "Free Economics 101 flashcards. Key concepts in micro and macroeconomics. Study online or import into Stacked.",
    "keywords": "economics flashcards, econ 101, economics study cards, microeconomics, macroeconomics",
    "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
    "cards": [
      ("Supply and Demand", "Price is determined where supply meets demand; if demand rises and supply stays, price increases"),
      ("GDP (Gross Domestic Product)", "Total value of all goods and services produced in a country in a given year; measures economic output"),
      ("Inflation", "General increase in prices over time; decreases purchasing power; measured by CPI"),
      ("Recession", "Two consecutive quarters of declining GDP; rising unemployment; reduced spending"),
      ("Opportunity Cost", "The value of the next best alternative given up when making a choice"),
      ("Scarcity", "Limited resources vs unlimited wants; the fundamental economic problem"),
      ("Elasticity", "How much quantity demanded/supplied changes when price changes; elastic = large change, inelastic = small change"),
      ("Monopoly", "Market with a single seller; no competition; can set prices; barriers to entry"),
      ("Perfect Competition", "Many sellers, identical products, no barriers to entry; price takers; theoretical ideal"),
      ("Oligopoly", "Market dominated by a few large firms; interdependent pricing; examples: airlines, telecom"),
      ("Fiscal Policy", "Government use of spending and taxation to influence the economy; done by Congress/Parliament"),
      ("Monetary Policy", "Central bank controls money supply and interest rates to manage the economy; done by the Fed"),
      ("Federal Reserve (The Fed)", "US central bank; sets interest rates; controls money supply; lender of last resort"),
      ("Interest Rate", "Cost of borrowing money; when rates rise, borrowing decreases; when rates fall, borrowing increases"),
      ("Comparative Advantage", "A country should produce goods where it has the lowest opportunity cost; basis for trade"),
      ("Marginal Cost", "The cost of producing one additional unit of a good"),
      ("Marginal Utility", "The additional satisfaction from consuming one more unit; diminishes with each additional unit"),
      ("Consumer Price Index (CPI)", "Measures average change in prices paid by consumers; used to calculate inflation rate"),
      ("Unemployment Rate", "Percentage of labor force that is jobless and actively seeking work"),
      ("Trade Deficit", "When a country imports more than it exports; opposite is trade surplus"),
      ("Externality", "Cost or benefit affecting a third party not involved in a transaction; positive or negative"),
      ("Public Good", "Non-excludable and non-rivalrous; examples: national defense, street lights; often provided by government"),
      ("Market Failure", "When free markets fail to allocate resources efficiently; caused by externalities, monopolies, or public goods"),
      ("Adam Smith", "Father of economics; wrote 'The Wealth of Nations' (1776); invisible hand theory; free market advocate"),
      ("John Maynard Keynes", "Advocated government intervention during recessions; Keynesian economics; influenced New Deal"),
      ("Law of Diminishing Returns", "Adding more of one input while holding others constant eventually yields smaller increases in output"),
      ("Budget Deficit", "When government spending exceeds revenue (taxes); adds to national debt"),
      ("Exchange Rate", "Price of one currency in terms of another; affects imports and exports"),
      ("Tariff", "Tax on imported goods; protects domestic industries; raises prices for consumers"),
      ("Subsidy", "Government payment to producers to lower costs and encourage production"),
    ]
  },
  {
    "slug": "computer-science-basics",
    "title": "Computer Science Basics",
    "category": "College",
    "description": "Fundamental computer science concepts including data structures, algorithms, and programming basics.",
    "meta_desc": "Free Computer Science flashcards. Key concepts in data structures, algorithms, and programming. Study online or import into Stacked.",
    "keywords": "computer science flashcards, CS 101, programming flashcards, data structures, algorithms",
    "color": {"hex": "#5AC8FA", "r": 0.353, "g": 0.784, "b": 0.980},
    "cards": [
      ("Algorithm", "A step-by-step procedure for solving a problem or accomplishing a task"),
      ("Variable", "A named storage location in memory that holds a value; can change during program execution"),
      ("Array", "An ordered collection of elements stored in contiguous memory; accessed by index; fixed size"),
      ("Loop", "Code that repeats execution; types: for loop (known iterations), while loop (condition-based)"),
      ("Function", "A reusable block of code that performs a specific task; takes inputs (parameters), returns output"),
      ("Conditional Statement", "Code that executes based on a condition; if/else/else if; controls program flow"),
      ("Boolean", "A data type with only two values: true or false; used in conditions and logic"),
      ("String", "A sequence of characters (text); immutable in many languages; enclosed in quotes"),
      ("Integer", "A whole number data type; no decimal point; positive, negative, or zero"),
      ("Binary", "Base-2 number system using 0s and 1s; how computers store all data"),
      ("Big O Notation", "Describes algorithm efficiency; O(1) constant, O(n) linear, O(n²) quadratic, O(log n) logarithmic"),
      ("Stack", "LIFO data structure (Last In, First Out); push adds, pop removes; like a stack of plates"),
      ("Queue", "FIFO data structure (First In, First Out); enqueue adds, dequeue removes; like a line of people"),
      ("Linked List", "Data structure where each element points to the next; dynamic size; no contiguous memory required"),
      ("Hash Table", "Key-value data structure; O(1) average lookup; handles collisions; used in dictionaries/maps"),
      ("Binary Tree", "Tree where each node has at most 2 children; binary search tree: left < parent < right"),
      ("Recursion", "A function that calls itself; needs a base case to stop; used for trees, fractals, divide-and-conquer"),
      ("Sorting Algorithms", "Bubble sort O(n²), merge sort O(n log n), quick sort O(n log n) avg; organize data in order"),
      ("Binary Search", "Efficient search on sorted data; divides in half each step; O(log n) time complexity"),
      ("Object-Oriented Programming", "Programming paradigm using objects with properties and methods; classes, inheritance, encapsulation, polymorphism"),
      ("Class", "A blueprint for creating objects; defines properties (attributes) and methods (behaviors)"),
      ("Inheritance", "A class can inherit properties and methods from a parent class; promotes code reuse"),
      ("API", "Application Programming Interface; defines how software components interact; request/response pattern"),
      ("HTTP Methods", "GET (retrieve), POST (create), PUT (update), DELETE (remove); used in web APIs"),
      ("Database", "Organized collection of data; SQL (relational tables) vs NoSQL (documents, key-value, graph)"),
      ("Git", "Version control system; tracks code changes; commands: commit, push, pull, branch, merge"),
      ("Compiler vs Interpreter", "Compiler: translates entire program before running; Interpreter: translates line by line during execution"),
      ("Bug", "An error in code; syntax error (won't compile), logic error (wrong result), runtime error (crashes)"),
      ("Testing", "Verifying code works correctly; unit tests (individual functions), integration tests (components together)"),
      ("Time Complexity", "How running time grows with input size; constant O(1) < logarithmic O(log n) < linear O(n) < quadratic O(n²)"),
    ]
  },
  {
    "slug": "ap-chemistry",
    "title": "AP Chemistry",
    "category": "AP Exams",
    "description": "Key concepts for AP Chemistry including atomic structure, bonding, reactions, and thermodynamics.",
    "meta_desc": "Free AP Chemistry flashcards. Key concepts for the AP Chem exam. Atomic structure, bonding, reactions. Study online or import into Stacked.",
    "keywords": "AP Chemistry flashcards, AP Chem review, AP Chemistry study cards, chemistry exam prep",
    "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
    "cards": [
      ("Atom", "Smallest unit of an element; consists of protons, neutrons (nucleus) and electrons (orbitals)"),
      ("Atomic Number", "Number of protons in an atom; defines the element; equals electrons in neutral atom"),
      ("Mass Number", "Protons + neutrons; isotopes have same atomic number but different mass numbers"),
      ("Electron Configuration", "Distribution of electrons in orbitals; follows Aufbau principle, Hund's rule, Pauli exclusion"),
      ("Ionic Bond", "Transfer of electrons between metals and nonmetals; creates cations (+) and anions (-)"),
      ("Covalent Bond", "Sharing of electron pairs between nonmetals; single, double, or triple bonds"),
      ("Electronegativity", "Atom's ability to attract shared electrons; increases across a period, decreases down a group"),
      ("Lewis Dot Structure", "Diagram showing valence electrons as dots; used to predict bonding and molecular shape"),
      ("VSEPR Theory", "Valence Shell Electron Pair Repulsion; predicts molecular geometry based on electron pairs"),
      ("Mole", "6.022 × 10²³ particles (Avogadro's number); bridge between atomic and macroscopic scale"),
      ("Molarity", "Concentration = moles of solute / liters of solution; units: mol/L or M"),
      ("Ideal Gas Law", "PV = nRT; P = pressure, V = volume, n = moles, R = gas constant, T = temperature (K)"),
      ("Stoichiometry", "Using balanced equations to calculate quantities of reactants and products; mole ratios"),
      ("Limiting Reagent", "Reactant completely consumed first; determines maximum amount of product formed"),
      ("Exothermic Reaction", "Releases energy/heat to surroundings; ΔH is negative; feels hot"),
      ("Endothermic Reaction", "Absorbs energy/heat from surroundings; ΔH is positive; feels cold"),
      ("Enthalpy (ΔH)", "Heat change at constant pressure; negative = exothermic, positive = endothermic"),
      ("Entropy (ΔS)", "Measure of disorder/randomness; tends to increase; gases > liquids > solids"),
      ("Gibbs Free Energy", "ΔG = ΔH - TΔS; negative ΔG = spontaneous reaction; positive ΔG = non-spontaneous"),
      ("Le Chatelier's Principle", "If a system at equilibrium is disturbed, it shifts to counteract the change"),
      ("Equilibrium Constant (K)", "Ratio of products to reactants at equilibrium; K > 1 favors products; K < 1 favors reactants"),
      ("Acids and Bases (Brønsted)", "Acid: proton (H⁺) donor; Base: proton acceptor; conjugate acid-base pairs"),
      ("pH Scale", "pH = -log[H⁺]; 0-14; 7 neutral; < 7 acidic; > 7 basic; each unit = 10x change"),
      ("Oxidation-Reduction (Redox)", "Oxidation: loss of electrons (OIL); Reduction: gain of electrons (RIG); occur together"),
      ("Oxidation Number", "Charge an atom would have if all bonds were ionic; tracks electron transfer"),
      ("Periodic Trends", "Atomic radius: increases down/left; Ionization energy: increases up/right; Electronegativity: increases up/right"),
      ("Intermolecular Forces", "London dispersion (weakest) < dipole-dipole < hydrogen bonding (strongest); affect boiling points"),
      ("Solubility Rules", "Like dissolves like; polar dissolves polar, nonpolar dissolves nonpolar; NaCl dissolves in water"),
      ("Reaction Rate", "Speed of a reaction; affected by temperature, concentration, surface area, catalysts"),
      ("Catalyst", "Speeds up reaction without being consumed; lowers activation energy; enzymes are biological catalysts"),
    ]
  },
  {
    "slug": "ap-world-history",
    "title": "AP World History",
    "category": "AP Exams",
    "description": "Key events, civilizations, and concepts for AP World History from ancient to modern times.",
    "meta_desc": "Free AP World History flashcards. Key events and civilizations from ancient to modern. Study for the AP World exam online.",
    "keywords": "AP World History flashcards, world history review, AP World study cards, history exam prep",
    "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
    "cards": [
      ("Mesopotamia", "Cradle of civilization; Tigris & Euphrates rivers; Sumerians, Babylonians, Assyrians; cuneiform writing"),
      ("Ancient Egypt", "Nile River civilization; pharaohs, pyramids, hieroglyphics; 3100-30 BCE; mummification"),
      ("Indus Valley Civilization", "Modern Pakistan/India; Harappa & Mohenjo-Daro; advanced urban planning; declined ~1900 BCE"),
      ("Ancient Greece", "Democracy, philosophy, art; Athens vs Sparta; Alexander the Great; Socrates, Plato, Aristotle"),
      ("Roman Empire", "Republic → Empire; law, engineering, roads; fell 476 CE (West); Christianity became state religion"),
      ("Silk Road", "Trade network connecting China to Mediterranean; spread goods, ideas, religion, and disease; ~130 BCE-1453 CE"),
      ("Islam's Golden Age", "8th-14th century; advances in math, science, medicine, philosophy; Baghdad, Córdoba; preserved Greek texts"),
      ("Tang Dynasty (618-907)", "Chinese golden age; poetry, art, trade; expanded Silk Road; Buddhism spread; civil service exams"),
      ("Feudalism", "Medieval social system: king → lords → vassals → serfs; land for military service; Europe and Japan"),
      ("Black Death (1347-1351)", "Bubonic plague killed 30-60% of Europe; spread via fleas/rats; led to labor shortages and social change"),
      ("Renaissance (14th-17th c.)", "Cultural rebirth in Europe; humanism; art (da Vinci, Michelangelo); began in Italian city-states"),
      ("Protestant Reformation", "Martin Luther's 95 Theses (1517); challenged Catholic Church; led to Protestantism; religious wars"),
      ("Age of Exploration", "15th-17th century; Europeans explored Americas, Africa, Asia; Columbus 1492; colonialism; Columbian Exchange"),
      ("Columbian Exchange", "Transfer of plants, animals, diseases between Old and New World after 1492; potatoes, horses, smallpox"),
      ("Atlantic Slave Trade", "16th-19th century; ~12 million Africans enslaved; triangular trade; Middle Passage; abolished gradually"),
      ("Scientific Revolution", "16th-17th century; Copernicus, Galileo, Newton; empirical method; challenged religious authority"),
      ("Enlightenment", "18th century intellectual movement; reason, liberty, progress; Locke, Voltaire, Rousseau; influenced revolutions"),
      ("French Revolution (1789)", "Overthrew monarchy; Liberty, Equality, Fraternity; Reign of Terror; Napoleon rose to power"),
      ("Industrial Revolution", "Late 18th century; factory system; steam power; urbanization; began in Britain; transformed economy"),
      ("Imperialism", "European colonization of Africa and Asia in 19th century; driven by resources, markets, nationalism"),
      ("World War I (1914-1918)", "Alliance system, nationalism, imperialism; trench warfare; Treaty of Versailles; 17 million dead"),
      ("Russian Revolution (1917)", "Overthrew Tsar Nicholas II; Bolsheviks led by Lenin; established communist Soviet Union"),
      ("World War II (1939-1945)", "Axis vs Allies; Holocaust; atomic bombs; 70-85 million dead; UN created; Cold War followed"),
      ("Decolonization", "Post-WWII independence movements in Asia and Africa; India 1947, African nations 1960s; end of empires"),
      ("Cold War (1947-1991)", "US vs USSR; capitalism vs communism; nuclear arms race; proxy wars; Berlin Wall fell 1989"),
      ("Globalization", "Increasing interconnection of world economies, cultures, and populations; driven by trade, technology, migration"),
      ("Mongol Empire", "Largest contiguous land empire; Genghis Khan; 13th-14th century; connected East and West; Pax Mongolica"),
      ("Ottoman Empire", "1299-1922; controlled SE Europe, Middle East, N. Africa; Constantinople (Istanbul); declined after WWI"),
      ("Mughal Empire", "1526-1857; ruled Indian subcontinent; Akbar promoted tolerance; built Taj Mahal; declined under British rule"),
      ("Meiji Restoration (1868)", "Japan modernized rapidly; ended feudalism; industrialized; became imperial power; defeated Russia 1905"),
    ]
  },
  {
    "slug": "italian-101",
    "title": "Italian 101 — Common Phrases",
    "category": "Languages",
    "description": "Essential Italian phrases and vocabulary for beginners and travelers visiting Italy.",
    "meta_desc": "Free Italian flashcards for beginners. Essential phrases and vocabulary words. Study online or import into Stacked.",
    "keywords": "Italian flashcards, learn Italian, Italian vocabulary, Italian 101, basic Italian phrases",
    "color": {"hex": "#30D158", "r": 0.188, "g": 0.820, "b": 0.345},
    "cards": [
      ("Hello", "Ciao"),
      ("Good morning", "Buongiorno"),
      ("Good evening", "Buonasera"),
      ("Goodbye", "Arrivederci"),
      ("Please", "Per favore"),
      ("Thank you", "Grazie"),
      ("You're welcome", "Prego"),
      ("Yes", "Sì"),
      ("No", "No"),
      ("Excuse me", "Scusi"),
      ("I'm sorry", "Mi dispiace"),
      ("How are you?", "Come stai?"),
      ("I'm fine", "Sto bene"),
      ("What is your name?", "Come ti chiami?"),
      ("My name is...", "Mi chiamo..."),
      ("I don't understand", "Non capisco"),
      ("Do you speak English?", "Parla inglese?"),
      ("Where is...?", "Dov'è...?"),
      ("How much?", "Quanto costa?"),
      ("Water", "Acqua"),
      ("Coffee", "Caffè"),
      ("Wine", "Vino"),
      ("The check, please", "Il conto, per favore"),
      ("Delicious", "Delizioso / Buonissimo"),
      ("I would like", "Vorrei"),
      ("One", "Uno"),
      ("Two", "Due"),
      ("Three", "Tre"),
      ("Beautiful", "Bello / Bella"),
      ("Love", "Amore"),
    ]
  },
  {
    "slug": "mandarin-basics",
    "title": "Mandarin Chinese — Basic Phrases",
    "category": "Languages",
    "description": "Essential Mandarin Chinese phrases with pinyin pronunciation for beginners.",
    "meta_desc": "Free Mandarin Chinese flashcards. Essential phrases with pinyin for beginners. Study online or import into Stacked.",
    "keywords": "Mandarin flashcards, learn Chinese, Chinese vocabulary, Mandarin basics, Chinese phrases",
    "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
    "cards": [
      ("Hello", "你好 (nǐ hǎo)"),
      ("Goodbye", "再见 (zài jiàn)"),
      ("Thank you", "谢谢 (xiè xie)"),
      ("You're welcome", "不客气 (bú kè qi)"),
      ("I'm sorry", "对不起 (duì bu qǐ)"),
      ("Yes / Correct", "是 / 对 (shì / duì)"),
      ("No / Incorrect", "不是 / 不对 (bú shì / bú duì)"),
      ("How are you?", "你好吗？(nǐ hǎo ma?)"),
      ("I'm fine", "我很好 (wǒ hěn hǎo)"),
      ("What is your name?", "你叫什么名字？(nǐ jiào shén me míng zi?)"),
      ("My name is...", "我叫... (wǒ jiào...)"),
      ("I don't understand", "我不懂 (wǒ bù dǒng)"),
      ("How much?", "多少钱？(duō shǎo qián?)"),
      ("Water", "水 (shuǐ)"),
      ("Food", "食物 (shí wù)"),
      ("One", "一 (yī)"),
      ("Two", "二 (èr)"),
      ("Three", "三 (sān)"),
      ("Four", "四 (sì)"),
      ("Five", "五 (wǔ)"),
      ("Six", "六 (liù)"),
      ("Seven", "七 (qī)"),
      ("Eight", "八 (bā)"),
      ("Nine", "九 (jiǔ)"),
      ("Ten", "十 (shí)"),
      ("I want", "我要 (wǒ yào)"),
      ("Good / Great", "好 (hǎo)"),
      ("Friend", "朋友 (péng yǒu)"),
      ("Love", "爱 (ài)"),
      ("China", "中国 (zhōng guó)"),
    ]
  },
  {
    "slug": "ap-government",
    "title": "AP US Government & Politics",
    "category": "AP Exams",
    "description": "Key concepts for AP Government including the Constitution, branches of government, and civil liberties.",
    "meta_desc": "Free AP Government flashcards. Constitution, branches, civil liberties. Study for the AP Gov exam online or import into Stacked.",
    "keywords": "AP Government flashcards, AP Gov review, US government study cards, civics flashcards",
    "color": {"hex": "#007AFF", "r": 0.0, "g": 0.478, "b": 1.0},
    "cards": [
      ("Federalism", "Division of power between national and state governments; enumerated vs reserved powers"),
      ("Separation of Powers", "Government divided into 3 branches: legislative, executive, judicial; prevents concentration of power"),
      ("Checks and Balances", "Each branch can limit the others; presidential veto, judicial review, Senate confirmation"),
      ("Judicial Review", "Supreme Court power to declare laws unconstitutional; established in Marbury v. Madison (1803)"),
      ("Bill of Rights", "First 10 amendments; protects individual rights: speech, religion, arms, fair trial, etc."),
      ("1st Amendment", "Freedom of religion, speech, press, assembly, and petition"),
      ("2nd Amendment", "Right to keep and bear arms"),
      ("4th Amendment", "Protection against unreasonable searches and seizures; requires warrants with probable cause"),
      ("5th Amendment", "Due process, double jeopardy, self-incrimination, eminent domain"),
      ("14th Amendment", "Equal protection, due process applied to states; citizenship clause; most-litigated amendment"),
      ("Electoral College", "538 electors; 270 needed to win; winner-take-all in most states; allocates electors by state population + 2"),
      ("Congressional Powers", "Article I; taxing, spending, commerce, declare war; Senate: treaties, confirmations; House: revenue bills, impeach"),
      ("Executive Powers", "Article II; Commander in Chief, pardons, treaties (with Senate), executive orders, veto"),
      ("Supreme Court", "9 justices; life tenure; original and appellate jurisdiction; cert petitions; precedent (stare decisis)"),
      ("Marbury v. Madison (1803)", "Established judicial review; Supreme Court can declare laws unconstitutional"),
      ("McCulloch v. Maryland (1819)", "Federal law supreme over state law; implied powers (Necessary and Proper Clause); can't tax federal bank"),
      ("Brown v. Board (1954)", "School segregation unconstitutional; overturned 'separate but equal' (Plessy v. Ferguson)"),
      ("Gideon v. Wainwright (1963)", "Right to an attorney in criminal cases, even if you can't afford one"),
      ("Miranda v. Arizona (1966)", "Must inform suspects of rights before interrogation (right to remain silent, right to attorney)"),
      ("Political Parties", "Two-party system; Democrats (left-center) and Republicans (right-center); third parties rarely win"),
      ("Interest Groups", "Organizations that influence policy; lobbying, PACs, grassroots campaigns; NRA, AARP, Sierra Club"),
      ("Gerrymandering", "Drawing district lines to favor a party; packing and cracking; affects representation"),
      ("Filibuster", "Senate tactic to delay a vote by extended debate; requires 60 votes for cloture to end"),
      ("Bureaucracy", "Federal agencies that implement laws; Cabinet departments, independent agencies; civil service system"),
      ("Iron Triangle", "Relationship between congressional committees, bureaucratic agencies, and interest groups; policy-making"),
      ("Civil Liberties", "Constitutional protections against government; Bill of Rights; individual freedoms"),
      ("Civil Rights", "Government protection of equal treatment; anti-discrimination laws; 14th Amendment equal protection"),
      ("Due Process", "Government must follow fair procedures before depriving life, liberty, or property; 5th and 14th Amendments"),
      ("Federalist Papers", "Hamilton, Madison, Jay; essays arguing for Constitution ratification; Federalist 10 (factions), 51 (checks)"),
      ("Amendments Process", "2/3 of both chambers propose, 3/4 of state legislatures ratify; or constitutional convention (never used)"),
    ]
  },
]

# HTML template for deck pages
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
    print(f"✅ {deck['slug']}.html ({len(deck['cards'])} cards)")

print(f"\n🎉 Generated {len(DECKS)} deck pages")

# Also output deck list for catalog page
catalog_data = []
for d in DECKS:
    catalog_data.append({
        "slug": d["slug"],
        "title": d["title"],
        "category": d["category"],
        "description": d["description"],
        "card_count": len(d["cards"]),
        "color": d["color"]["hex"],
    })
with open(os.path.join(SITE, "decks", "catalog.json"), "w") as f:
    json.dump(catalog_data, f, indent=2)
print("✅ catalog.json")
