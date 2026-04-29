#!/usr/bin/env python3
"""Generate 3 organic chemistry deck HTML pages and update catalog.json."""
import json, html, os, sys

# Add parent dir to import the TEMPLATE
sys.path.insert(0, "/Users/stephaniedugas/Documents/stacked-site")
from importlib import import_module

SITE = "/Users/stephaniedugas/Documents/stacked-site"

# ─── DECK 1: Functional Groups & Nomenclature (50 cards) ───
FUNCTIONAL_GROUPS_CARDS = [
    ("What is the functional group, suffix, and general formula for ALKANES?",
     "C\u2013C and C\u2013H single bonds only. Suffix: -ane. General formula: C\u2099H\u2082\u2099\u208a\u2082. Saturated hydrocarbons. Example: ethane (CH\u2083CH\u2083)."),

    ("What is the functional group, suffix, and general formula for ALKENES?",
     "C=C double bond. Suffix: -ene. General formula: C\u2099H\u2082\u2099. One degree of unsaturation. Example: ethene (CH\u2082=CH\u2082)."),

    ("What is the functional group, suffix, and general formula for ALKYNES?",
     "C\u2261C triple bond. Suffix: -yne. General formula: C\u2099H\u2082\u2099\u208b\u2082. Two degrees of unsaturation. Example: ethyne (HC\u2261CH, acetylene)."),

    ("What is the functional group, suffix, and general formula for ALCOHOLS?",
     "\u2013OH (hydroxyl group). Suffix: -ol. General formula: R\u2013OH. Classified as 1\u00b0 (\u2013CH\u2082OH), 2\u00b0 (R\u2082CHOH), or 3\u00b0 (R\u2083COH). Example: ethanol (CH\u2083CH\u2082OH)."),

    ("What is the functional group, suffix, and general formula for ETHERS?",
     "R\u2013O\u2013R\u2019. No dedicated IUPAC suffix \u2014 named as alkoxy substituents (prefix: alkoxy-). Common name format: alkyl alkyl ether. Example: diethyl ether (CH\u2083CH\u2082OCH\u2082CH\u2083), IUPAC: ethoxyethane."),

    ("What is the functional group, suffix, and general formula for ALDEHYDES?",
     "\u2013CHO (carbonyl at terminal carbon). Suffix: -al. General formula: RCHO. The carbonyl carbon has at least one H. Example: ethanal (CH\u2083CHO, acetaldehyde)."),

    ("What is the functional group, suffix, and general formula for KETONES?",
     "C=O (carbonyl between two carbons). Suffix: -one. General formula: RCOR\u2019. Example: propanone (CH\u2083COCH\u2083, acetone)."),

    ("What is the functional group, suffix, and general formula for CARBOXYLIC ACIDS?",
     "\u2013COOH (carboxyl group). Suffix: -oic acid. General formula: RCOOH. Example: ethanoic acid (CH\u2083COOH, acetic acid). Highest IUPAC naming priority of common functional groups."),

    ("What is the functional group, suffix, and general formula for ESTERS?",
     "\u2013COOR\u2019 (carbonyl bonded to \u2013OR\u2019). Suffix: -oate. Named as alkyl alkanoate. Example: ethyl ethanoate (CH\u2083COOCH\u2082CH\u2083, ethyl acetate)."),

    ("What is the functional group, suffix, and general formula for AMIDES?",
     "\u2013CONR\u2082 (carbonyl bonded to nitrogen). Suffix: -amide. Example: ethanamide (CH\u2083CONH\u2082, acetamide). N-substituents indicated with N- prefix."),

    ("What is the functional group, suffix, and general formula for AMINES?",
     "\u2013NR\u2082 (amino group). Suffix: -amine. Classified as 1\u00b0 (RNH\u2082), 2\u00b0 (R\u2082NH), 3\u00b0 (R\u2083N). Example: ethanamine (CH\u2083CH\u2082NH\u2082). Note: classification is by number of C groups on N, not the carbon classification."),

    ("What is the functional group, suffix, and general formula for THIOLS?",
     "\u2013SH (sulfhydryl group). Suffix: -thiol. General formula: R\u2013SH. Sulfur analog of alcohols. Lower boiling points than alcohols (weaker H-bonding). Strong, unpleasant odor. Example: ethanethiol (CH\u2083CH\u2082SH)."),

    ("What is the functional group, suffix, and general formula for ACID HALIDES (ACYL HALIDES)?",
     "\u2013COX (carbonyl bonded to halogen). Suffix: -oyl halide. Very reactive \u2014 most reactive carboxylic acid derivative. Example: ethanoyl chloride (CH\u2083COCl, acetyl chloride)."),

    ("What is the functional group, suffix, and general formula for ACID ANHYDRIDES?",
     "RCO\u2013O\u2013COR\u2019 (two acyl groups joined by oxygen). Suffix: -oic anhydride. Example: ethanoic anhydride ((CH\u2083CO)\u2082O, acetic anhydride). More reactive than esters, less reactive than acid halides."),

    ("What is the functional group, suffix, and general formula for NITRILES?",
     "\u2013C\u2261N (triple bond to nitrogen). Suffix: -nitrile (IUPAC) or -carbonitrile (when C\u2261N is not part of parent chain). The nitrile carbon is counted in the parent chain. Example: ethanenitrile (CH\u2083CN, acetonitrile)."),

    ("What are the step-by-step IUPAC naming rules for organic compounds?",
     "1) Find the LONGEST continuous carbon chain containing the highest-priority functional group \u2014 this is the parent chain.\n2) Number the chain to give the highest-priority functional group the LOWEST locant.\n3) Identify and name all substituents (alkyl groups, halogens).\n4) Assign locants to each substituent.\n5) List substituents ALPHABETICALLY (ignore di-, tri- prefixes for alphabetization).\n6) Use di-, tri-, tetra- for identical substituents.\n7) Use commas between numbers and hyphens between numbers and words."),

    ("What is the IUPAC priority order for functional groups when naming polyfunctional compounds?",
     "Highest to lowest priority (as principal characteristic group):\n1. Carboxylic acid (-oic acid)\n2. Acid anhydride (-oic anhydride)\n3. Ester (-oate)\n4. Acid halide (-oyl halide)\n5. Amide (-amide)\n6. Nitrile (-nitrile)\n7. Aldehyde (-al)\n8. Ketone (-one)\n9. Alcohol (-ol)\n10. Amine (-amine)\n11. Alkene (-ene)\n12. Alkyne (-yne)\nLower-priority groups become prefixes (e.g., hydroxy-, oxo-, amino-)."),

    ("How do you name a compound with MULTIPLE SUBSTITUENTS on the parent chain?",
     "List substituents alphabetically. Use di-, tri-, tetra- for repeated identical substituents. Separate locants with commas and locants from names with hyphens. Example: 2,4-dimethyl-3-ethylhexane \u2192 listed as 3-ethyl-2,4-dimethylhexane (ethyl before methyl alphabetically; \u2018di\u2019 is ignored for alphabetization)."),

    ("How do you name CYCLIC compounds in IUPAC nomenclature?",
     "Add prefix \u2018cyclo-\u2019 before the parent name. Number the ring to give substituents lowest locants. If only one substituent, no locant needed. If the ring has a functional group (e.g., -ol), that carbon is C1. Example: 3-methylcyclohexanol (OH at C1, methyl at C3). If the chain attached to the ring has more carbons than the ring, the ring becomes a substituent (e.g., cyclohexylheptane)."),

    ("How do you name ALKENES with cis/trans and E/Z designations?",
     "cis/trans: Only for disubstituted alkenes. cis = same side, trans = opposite side.\nE/Z: Works for ALL alkenes. Assign priorities using CIP rules on each carbon of the double bond. Z (zusammen) = higher-priority groups on SAME side. E (entgegen) = higher-priority groups on OPPOSITE side.\nThe double bond gets the lowest possible locant. Suffix: -ene."),

    ("How do you name and classify ALCOHOLS as 1\u00b0, 2\u00b0, or 3\u00b0?",
     "Classification depends on the carbon bearing the \u2013OH:\n1\u00b0 alcohol: \u2013OH on a carbon bonded to ONE other carbon (e.g., 1-propanol, CH\u2083CH\u2082CH\u2082OH).\n2\u00b0 alcohol: \u2013OH on a carbon bonded to TWO other carbons (e.g., 2-propanol, (CH\u2083)\u2082CHOH).\n3\u00b0 alcohol: \u2013OH on a carbon bonded to THREE other carbons (e.g., 2-methyl-2-propanol, (CH\u2083)\u2083COH).\nThe \u2013OH carbon gets the lowest locant in the parent chain. Suffix: -ol."),

    ("How do you name AMINES in IUPAC nomenclature?",
     "Suffix: -amine. The parent chain includes the carbon bearing \u2013NH\u2082. Number to give N the lowest locant. For secondary/tertiary amines, substituents on nitrogen get the prefix N- (e.g., N-methylethanamine for CH\u2083NHCH\u2082CH\u2083). Classification: 1\u00b0 = RNH\u2082, 2\u00b0 = R\u2082NH, 3\u00b0 = R\u2083N."),

    ("What are the common names for these aldehydes: HCHO, CH\u2083CHO, C\u2086H\u2085CHO?",
     "HCHO = formaldehyde (IUPAC: methanal)\nCH\u2083CHO = acetaldehyde (IUPAC: ethanal)\nC\u2086H\u2085CHO = benzaldehyde (IUPAC: benzaldehyde \u2014 common name retained in IUPAC)"),

    ("What are the common names for these ketones/acids: CH\u2083COCH\u2083, CH\u2083COOH, HCOOH?",
     "CH\u2083COCH\u2083 = acetone (IUPAC: propanone)\nCH\u2083COOH = acetic acid (IUPAC: ethanoic acid)\nHCOOH = formic acid (IUPAC: methanoic acid)"),

    ("What are the common names for: CH\u2083OH, CH\u2083CH\u2082OH, (CH\u2083)\u2082CHOH, C\u2086H\u2085OH?",
     "CH\u2083OH = methyl alcohol / methanol (wood alcohol)\nCH\u2083CH\u2082OH = ethyl alcohol / ethanol (grain alcohol)\n(CH\u2083)\u2082CHOH = isopropyl alcohol / 2-propanol (rubbing alcohol)\nC\u2086H\u2085OH = phenol (not an alcohol \u2014 special aromatic compound, more acidic than typical alcohols)"),

    ("What are the common names for: CH\u2082=CH\u2082, CH\u2082=CHCH\u2083, CH\u2083C\u2261CH?",
     "CH\u2082=CH\u2082 = ethylene (IUPAC: ethene)\nCH\u2082=CHCH\u2083 = propylene (IUPAC: propene)\nCH\u2083C\u2261CH = methylacetylene (IUPAC: propyne)\nHC\u2261CH = acetylene (IUPAC: ethyne)"),

    ("What is the common name for CH\u2083OCH\u2083 and what is the common name for (CH\u2083CH\u2082)\u2082O?",
     "CH\u2083OCH\u2083 = dimethyl ether (IUPAC: methoxymethane)\n(CH\u2083CH\u2082)\u2082O = diethyl ether (IUPAC: ethoxyethane). Common ether naming: list both alkyl groups alphabetically + \u2018ether\u2019."),

    ("What are the common names for CH\u2083CONH\u2082 and CH\u2083CN?",
     "CH\u2083CONH\u2082 = acetamide (IUPAC: ethanamide)\nCH\u2083CN = acetonitrile (IUPAC: ethanenitrile)"),

    ("Rank the following by BOILING POINT (highest to lowest): alkane, alcohol, carboxylic acid, amine, ether, ketone (all ~same molecular weight). Explain why.",
     "Carboxylic acid > alcohol > amine (1\u00b0) > ketone \u2248 aldehyde > ether > alkane.\nReasoning:\n- Carboxylic acids form strong DIMERIC hydrogen bonds (two H-bonds per pair).\n- Alcohols form strong H-bonds (O\u2013H).\n- 1\u00b0 Amines form moderate H-bonds (N\u2013H, N is less electronegative than O).\n- Ketones/aldehydes have dipole-dipole interactions (C=O is polar but can\u2019t donate H-bonds to themselves).\n- Ethers have weak dipole-dipole only.\n- Alkanes have only London dispersion forces."),

    ("Which functional groups are SOLUBLE in water and why?",
     "Soluble (low MW, \u22644-5 carbons): alcohols, carboxylic acids, amines, aldehydes, ketones \u2014 they can hydrogen bond with water.\nGenerally insoluble: alkanes, alkyl halides, ethers (slightly soluble \u2014 can accept H-bonds but not donate).\nRule of thumb: compounds with \u22644-5 carbons and an H-bond donor/acceptor are water-soluble. As carbon chain grows, hydrophobic character dominates."),

    ("What intermolecular forces do ALCOHOLS exhibit? How does this affect their properties?",
     "Hydrogen bonding (O\u2013H\u00b7\u00b7\u00b7O), dipole-dipole, and London dispersion forces. The strong H-bonding gives alcohols: higher boiling points than similar MW ethers/alkanes, water solubility (small alcohols), and the ability to act as both H-bond donors and acceptors."),

    ("What intermolecular forces do KETONES and ALDEHYDES exhibit?",
     "Dipole-dipole interactions (from the polar C=O bond) and London dispersion forces. They can accept hydrogen bonds from water (lone pairs on O) but CANNOT donate H-bonds to each other (no O\u2013H or N\u2013H). This makes them lower boiling than alcohols but higher than ethers of similar MW."),

    ("What intermolecular forces do ALKANES exhibit?",
     "ONLY London dispersion forces (induced dipole-induced dipole). These are the weakest IMFs. Consequence: alkanes have the lowest boiling points among organic compounds of similar MW, are nonpolar, insoluble in water, and soluble in nonpolar solvents. Branching lowers BP (less surface area for LDF contact)."),

    ("What intermolecular forces do CARBOXYLIC ACIDS exhibit? Why do they have unusually high boiling points?",
     "Strong hydrogen bonding \u2014 carboxylic acids form DIMERS through two simultaneous H-bonds between two \u2013COOH groups (cyclic dimer). Also dipole-dipole and London dispersion. This dimerization effectively doubles the molecular weight in solution, giving unusually high boiling points (e.g., acetic acid bp = 118\u00b0C vs acetone bp = 56\u00b0C, despite similar MW)."),

    ("Rank these functional groups by ACIDITY (most to least acidic).",
     "Most acidic \u2192 least acidic:\n1. Sulfonic acid (RSO\u2083H), pKa \u2248 -1\n2. Carboxylic acid (RCOOH), pKa \u2248 4-5\n3. Phenol (ArOH), pKa \u2248 10\n4. Thiol (RSH), pKa \u2248 10-11\n5. Water (H\u2082O), pKa = 15.7\n6. Alcohol (ROH), pKa \u2248 16-18\n7. Terminal alkyne (RC\u2261CH), pKa \u2248 25\n8. Amine (RNH\u2082), pKa \u2248 38 (of N\u2013H)\n9. Alkane (R\u2013H), pKa \u2248 50\nKey: Acidity increases with stability of conjugate base (resonance, electronegativity, size of atom)."),

    ("Why are carboxylic acids more acidic than alcohols?",
     "The conjugate base of a carboxylic acid (carboxylate, RCOO\u207b) is stabilized by RESONANCE \u2014 the negative charge is delocalized equally over two oxygen atoms. The conjugate base of an alcohol (alkoxide, RO\u207b) has the negative charge localized on one oxygen with no resonance stabilization. Greater conjugate base stability = stronger acid."),

    ("Why are phenols more acidic than alcohols but less acidic than carboxylic acids?",
     "Phenol\u2019s conjugate base (phenoxide, ArO\u207b) is stabilized by resonance with the aromatic ring \u2014 the negative charge delocalizes into the ring (4 resonance structures). This is better than an alkoxide (no resonance) but worse than a carboxylate (charge delocalized over two equivalent oxygens). Electron-withdrawing groups on the ring increase phenol acidity further."),

    ("What is the DEGREES OF UNSATURATION (index of hydrogen deficiency) formula? How do you use it?",
     "Formula: DoU = (2C + 2 + N - H - X) / 2\nWhere C = carbons, N = nitrogens, H = hydrogens, X = halogens. Oxygen and sulfur are NOT counted.\nEach DoU = one ring OR one double bond. Two DoU could be one triple bond, two double bonds, two rings, or one ring + one double bond.\nExample: C\u2086H\u2086 \u2192 DoU = (12 + 2 - 6) / 2 = 4 \u2192 benzene (3 double bonds + 1 ring = 4)."),

    ("What is the difference between CONSTITUTIONAL ISOMERS and STEREOISOMERS?",
     "Constitutional (structural) isomers: Same molecular formula, DIFFERENT connectivity of atoms. Example: butanol vs diethyl ether (C\u2084H\u2081\u2080O).\nStereoisomers: Same molecular formula AND same connectivity, but DIFFERENT 3D arrangement. Two subtypes: enantiomers (non-superimposable mirror images) and diastereomers (stereoisomers that are NOT mirror images, including cis/trans isomers)."),

    ("Calculate the degrees of unsaturation for C\u2088H\u2088O\u2083 and suggest possible structures.",
     "DoU = (2\u00d78 + 2 - 8) / 2 = 10/2 = 5. Oxygen is ignored in the formula.\n5 DoU suggests a benzene ring (4 DoU: 3 double bonds + 1 ring) plus one additional DoU (one more double bond or ring). Possible structure: vanillin (4-hydroxy-3-methoxybenzaldehyde) \u2014 aromatic ring (4 DoU) + aldehyde C=O (1 DoU) = 5 DoU."),

    ("How do you determine the degrees of unsaturation for a compound containing a halogen? Example: C\u2083H\u2085ClO",
     "Treat each halogen (F, Cl, Br, I) as one hydrogen in the formula. DoU = (2\u00d73 + 2 - 5 - 1) / 2 = (6 + 2 - 6) / 2 = 1. One DoU means one ring or one double bond. Possible structure: 3-chloropropanal (ClCH\u2082CH\u2082CHO) \u2014 one C=O double bond."),

    ("What are the first 10 IUPAC parent chain prefixes?",
     "1C = meth-\n2C = eth-\n3C = prop-\n4C = but-\n5C = pent-\n6C = hex-\n7C = hept-\n8C = oct-\n9C = non-\n10C = dec-"),

    ("What are the common ALKYL SUBSTITUENT names you must know?",
     "\u2013CH\u2083 = methyl\n\u2013CH\u2082CH\u2083 = ethyl\n\u2013CH\u2082CH\u2082CH\u2083 = propyl (n-propyl)\n\u2013CH(CH\u2083)\u2082 = isopropyl (1-methylethyl)\n\u2013CH\u2082CH\u2082CH\u2082CH\u2083 = butyl (n-butyl)\n\u2013CH\u2082CH(CH\u2083)\u2082 = isobutyl (2-methylpropyl)\n\u2013CH(CH\u2083)CH\u2082CH\u2083 = sec-butyl (1-methylpropyl)\n\u2013C(CH\u2083)\u2083 = tert-butyl (1,1-dimethylethyl)"),

    ("How are HALOGENS named as substituents in IUPAC nomenclature?",
     "F = fluoro\nCl = chloro\nBr = bromo\nI = iodo\nHalogens are always treated as substituents (prefixes), never as the parent chain functional group. They are alphabetized with other substituents. Example: 2-bromo-3-chlorobutane (bromo listed before chloro alphabetically)."),

    ("Name this compound: CH\u2083CH\u2082CH(CH\u2083)CH\u2082CH(OH)CH\u2083",
     "Step 1: Longest chain containing \u2013OH = 6 carbons = hexan-\nStep 2: Number from end nearest to \u2013OH \u2192 OH at C2\nStep 3: Methyl branch at C4\nName: 4-methylhexan-2-ol\n(Note: IUPAC 2013 recommendation places locant immediately before the part of the name it relates to: hexan-2-ol rather than 2-hexanol.)"),

    ("What does the prefix \u2018iso-\u2019 mean in common nomenclature?",
     "\u2018Iso-\u2019 indicates a methyl branch at the end of the chain (penultimate carbon). Examples: isopropyl = \u2013CH(CH\u2083)\u2082, isobutyl = \u2013CH\u2082CH(CH\u2083)\u2082, isobutane = 2-methylpropane, isopentane = 2-methylbutane. It always means a (CH\u2083)\u2082CH\u2013 group at one end of the molecule."),

    ("What does \u2018neo-\u2019 and \u2018tert-\u2019 mean in common nomenclature?",
     "\u2018tert-\u2019 (tertiary): The point of attachment is a tertiary carbon. Example: tert-butyl = \u2013C(CH\u2083)\u2083.\n\u2018neo-\u2019: A quaternary carbon at the second-to-last position. Example: neopentane = 2,2-dimethylpropane = C(CH\u2083)\u2084."),

    ("How do you name BICYCLIC compounds?",
     "Use \u2018bicyclo[x.y.z]alkane\u2019 format where x \u2265 y \u2265 z are the number of carbons in each bridge (not counting bridgehead carbons). Total carbons = x + y + z + 2 (bridgehead carbons). Example: norbornane = bicyclo[2.2.1]heptane (2+2+1+2 = 7 carbons)."),

    ("How do you name compounds with both a double bond and an alcohol?",
     "The alcohol (\u2013ol) takes priority over the alkene (\u2013ene) for numbering. Combined suffix: -en-ol. Example: CH\u2082=CHCH\u2082OH = prop-2-en-1-ol (2-propen-1-ol). Number to give \u2013OH the lowest locant, then give the double bond the lowest remaining locant."),

    ("What is the difference between PRIMARY, SECONDARY, and TERTIARY designations for carbons, alcohols, and amines?",
     "CARBON classification: Based on how many other carbons are attached. 1\u00b0 = bonded to 1 other C, 2\u00b0 = 2 other C, 3\u00b0 = 3 other C.\nALCOHOL classification: Follows the carbon classification of the C bearing \u2013OH.\nAMINE classification: Based on number of C groups bonded to NITROGEN. 1\u00b0 = RNH\u2082, 2\u00b0 = R\u2082NH, 3\u00b0 = R\u2083N.\nIMPORTANT: A 3\u00b0 alcohol (like tert-butanol) and a 3\u00b0 amine (like triethylamine) use different classification logic!"),

    ("What is the suffix and structure for an EPOXIDE?",
     "An epoxide (oxirane) is a 3-membered ring containing one oxygen. IUPAC name: use \u2018oxirane\u2019 as parent or \u2018epoxyalkane.\u2019 Common naming: ___ene oxide (from the alkene it derives from). Example: ethylene oxide = oxirane. Highly strained ring (\u224860\u00b0 bond angles vs 109.5\u00b0) making it very reactive toward ring-opening."),

    ("How do you name DISUBSTITUTED BENZENE rings?",
     "Use ortho- (o-), meta- (m-), para- (p-) prefixes OR 1,2- / 1,3- / 1,4- numbering.\northo (o-) = 1,2-disubstituted (adjacent)\nmeta (m-) = 1,3-disubstituted\npara (p-) = 1,4-disubstituted (opposite)\nExample: p-dichlorobenzene = 1,4-dichlorobenzene.\nIf substituents differ, number to give the alphabetically first substituent the lower number, OR use the special base name if one exists (e.g., toluene, phenol, aniline)."),
]

# ─── DECK 2: Reactions & Mechanisms (60 cards) ───
REACTIONS_CARDS = [
    # SN2
    ("Describe the SN2 mechanism: steps, stereochemistry, rate law, and energy diagram.",
     "SN2 = Substitution, Nucleophilic, Bimolecular.\nMechanism: ONE concerted step \u2014 nucleophile attacks the electrophilic carbon from the BACKSIDE (180\u00b0 from leaving group) while the leaving group departs simultaneously.\nStereochemistry: INVERSION of configuration (Walden inversion) \u2014 100% inversion at the stereocenter.\nRate law: Rate = k[substrate][nucleophile] \u2014 second order (bimolecular).\nEnergy diagram: Single transition state (no intermediate), one energy maximum."),

    ("What conditions FAVOR SN2 reactions?",
     "1. Substrate: Methyl > 1\u00b0 > 2\u00b0 (3\u00b0 never \u2014 too sterically hindered).\n2. Nucleophile: STRONG nucleophile required (e.g., CN\u207b, I\u207b, RS\u207b, HO\u207b).\n3. Leaving group: Good leaving group (weak base after leaving: I\u207b > Br\u207b > Cl\u207b > F\u207b).\n4. Solvent: POLAR APROTIC solvent (DMSO, DMF, acetone, acetonitrile) \u2014 these don\u2019t solvate/stabilize the nucleophile, keeping it reactive.\n5. Concentration: High [Nu:] matters (it\u2019s in the rate law)."),

    # SN1
    ("Describe the SN1 mechanism: steps, stereochemistry, rate law, and energy diagram.",
     "SN1 = Substitution, Nucleophilic, Unimolecular.\nStep 1: Leaving group departs \u2192 forms CARBOCATION (rate-determining step).\nStep 2: Nucleophile attacks carbocation from EITHER face.\nStereochemistry: RACEMIZATION \u2014 mixture of retention and inversion. Typically slight excess of inversion (~55/45) due to ion pair shielding.\nRate law: Rate = k[substrate] \u2014 first order (unimolecular). Nucleophile not in rate law.\nEnergy diagram: TWO transition states with a carbocation intermediate (energy minimum) between them."),

    ("What conditions FAVOR SN1 reactions?",
     "1. Substrate: 3\u00b0 > 2\u00b0 >> 1\u00b0 (never methyl). Stable carbocations required.\n2. Nucleophile: WEAK nucleophile is fine (e.g., H\u2082O, ROH) \u2014 it\u2019s not in the rate law.\n3. Leaving group: Good leaving group needed (same trend as SN2).\n4. Solvent: POLAR PROTIC solvent (water, methanol, ethanol, acetic acid) \u2014 stabilizes carbocation intermediate and leaving group through solvation.\n5. Carbocation stability: 3\u00b0 > 2\u00b0 > 1\u00b0. Resonance-stabilized (allylic, benzylic) also favored."),

    # E2
    ("Describe the E2 mechanism: steps, stereochemistry, and rate law.",
     "E2 = Elimination, Bimolecular.\nMechanism: ONE concerted step \u2014 strong base abstracts a \u03b2-hydrogen while the leaving group departs simultaneously. Requires ANTI-PERIPLANAR geometry (H and LG are 180\u00b0 dihedral).\nStereochemistry: Stereochemistry is determined by the anti-periplanar requirement; for many substrates the trans (E) product predominates, but this is substrate-dependent, not an inherent rule.\nRate law: Rate = k[substrate][base] \u2014 second order.\nProduct: Zaitsev product usually favored (most substituted alkene) unless bulky base used."),

    ("What conditions FAVOR E2 reactions?",
     "1. Substrate: 3\u00b0 > 2\u00b0 > 1\u00b0 (rate). Works on all substrates but competes with SN2 for 1\u00b0 and 2\u00b0.\n2. Base: STRONG, often BULKY base (e.g., t-BuOK, DBU, LDA). Bulky bases favor E2 over SN2.\n3. Temperature: HIGH temperature favors elimination over substitution.\n4. Anti-periplanar geometry required \u2014 in cyclohexanes, H and LG must both be axial (trans-diaxial).\n5. Zaitsev rule: Most substituted alkene favored unless bulky base \u2192 Hofmann product (less substituted)."),

    # E1
    ("Describe the E1 mechanism: steps, stereochemistry, and rate law.",
     "E1 = Elimination, Unimolecular.\nStep 1: Leaving group departs \u2192 forms CARBOCATION (rate-determining step, same as SN1).\nStep 2: A base (often solvent) abstracts a \u03b2-hydrogen \u2192 forms alkene.\nStereochemistry: Not stereospecific (carbocation is planar, \u03b2-H can be removed from any position). Mixture of E and Z possible.\nRate law: Rate = k[substrate] \u2014 first order.\nProduct: Zaitsev product favored (most substituted, most stable alkene). Often competes with SN1."),

    ("What conditions FAVOR E1 reactions?",
     "Same conditions as SN1 (they always compete):\n1. Substrate: 3\u00b0 > 2\u00b0. Stable carbocations needed.\n2. Base: WEAK base (or no base \u2014 solvent acts as base).\n3. Solvent: Polar protic.\n4. Temperature: HIGHER temperature shifts SN1/E1 competition toward E1 (elimination is entropically favored \u2014 \u0394S is positive because 1 molecule \u2192 2 molecules).\n5. E1 always accompanied by SN1. Pure E1 is rare."),

    # Decision Framework
    ("Given a 3\u00b0 substrate with a strong base: predict SN1/SN2/E1/E2.",
     "E2. Reasoning: 3\u00b0 substrates are too sterically hindered for SN2 (backside attack blocked). Strong base drives E2 (bimolecular elimination). Even though 3\u00b0 substrates can do SN1/E1, the STRONG BASE dominates the pathway \u2192 E2 wins."),

    ("Given a 1\u00b0 substrate with a strong nucleophile/weak base in polar aprotic solvent: predict SN1/SN2/E1/E2.",
     "SN2. Reasoning: 1\u00b0 substrate is unhindered (good for backside attack). Strong nucleophile is in the rate law for SN2. Polar aprotic solvent doesn\u2019t solvate the nucleophile, keeping it reactive. Weak base means elimination is not competitive."),

    ("Given a 3\u00b0 substrate with a weak nucleophile in polar protic solvent at high temperature: predict.",
     "E1 (major) + SN1 (minor). Reasoning: 3\u00b0 substrate \u2192 cannot do SN2. Weak nucleophile \u2192 not E2. Polar protic solvent \u2192 favors carbocation formation (SN1/E1 conditions). High temperature \u2192 shifts equilibrium toward elimination (E1 > SN1)."),

    ("Given a 2\u00b0 substrate with a strong bulky base (like t-BuOK): predict.",
     "E2. Reasoning: 2\u00b0 substrate can do multiple pathways. Strong base \u2192 E2 favored over E1. Bulky base \u2192 cannot easily attack carbon for SN2, instead abstracts the more accessible \u03b2-hydrogen. E2 gives Hofmann product (less substituted alkene) with bulky bases."),

    ("How does the nucleophile/base distinction determine SN vs E?",
     "NUCLEOPHILE = attacks CARBON (substitution). BASE = attacks HYDROGEN (elimination).\nStrong nucleophile + weak base \u2192 SN2 (e.g., I\u207b, RS\u207b, CN\u207b, N\u2083\u207b)\nStrong base + weak nucleophile \u2192 E2 (e.g., t-BuO\u207b, LDA, DBN)\nStrong nucleophile + strong base \u2192 SN2 or E2 depending on substrate and temperature (e.g., HO\u207b, EtO\u207b \u2014 these are BOTH strong Nu and strong base; 1\u00b0 \u2192 SN2, 3\u00b0 \u2192 E2, 2\u00b0 \u2192 mixture)\nWeak nucleophile + weak base \u2192 SN1/E1 (e.g., H\u2082O, ROH)"),

    # Addition Reactions
    ("What is Markovnikov\u2019s Rule? Give the mechanism for HBr addition to propene.",
     "Markovnikov\u2019s Rule: In addition of HX to an unsymmetrical alkene, H adds to the LESS substituted carbon (the one with MORE H\u2019s already), and X adds to the MORE substituted carbon.\nMechanism (propene + HBr):\n1. Protonation: \u03c0 electrons attack H\u207a of HBr \u2192 form the MORE STABLE carbocation (2\u00b0 at C2, not 1\u00b0 at C1).\n2. Nucleophilic attack: Br\u207b attacks the carbocation at C2.\nProduct: 2-bromopropane (CH\u2083CHBrCH\u2083).\nRationale: The reaction goes through the most stable carbocation intermediate."),

    ("What is anti-Markovnikov addition? Give two examples with reagents.",
     "Anti-Markovnikov: The nucleophilic group adds to the LESS substituted carbon of the alkene.\n1. HBr + ROOR (peroxides): Radical chain mechanism. Br\u2022 adds first (anti-Mark), then H. Only works with HBr (not HCl or HI). Product: 1-bromopropane from propene.\n2. Hydroboration-oxidation (BH\u2083\u00b7THF, then H\u2082O\u2082/NaOH): BH\u2083 adds B to less substituted carbon (syn addition). Oxidation replaces B with OH. Overall: anti-Markovnikov, SYN addition of water. Product: 1-propanol from propene."),

    ("Describe halogenation of alkenes (Br\u2082 addition). What is the stereochemistry?",
     "Reagent: Br\u2082 (often in CH\u2082Cl\u2082 or CCl\u2084).\nMechanism:\n1. Alkene \u03c0 electrons attack Br\u2082 \u2192 form cyclic BROMONIUM ION intermediate + Br\u207b.\n2. Br\u207b attacks from the OPPOSITE face of the bromonium ion (backside attack, like SN2).\nStereochemistry: ANTI addition \u2014 the two Br atoms end up on opposite faces. This means trans-product from a cyclic alkene.\nProduct: vicinal dibromide. This reaction is also a TEST for unsaturation (Br\u2082/CCl\u2084 decolorizes)."),

    ("What is catalytic hydrogenation? Reagents and stereochemistry?",
     "Reagent: H\u2082 gas with a metal catalyst (Pd/C, Pt/C, or Ni).\nReaction: Adds H\u2082 across a double bond (or triple bond) \u2014 reduces alkenes to alkanes.\nStereochemistry: SYN addition \u2014 both H atoms add to the same face of the alkene (because both H atoms are delivered from the catalyst surface).\nNote: Pd/C with H\u2082 reduces C=C but usually NOT C=O. Lindlar\u2019s catalyst (Pd/CaCO\u2083, poisoned) reduces alkynes to CIS alkenes only (partial reduction)."),

    ("What does mCPBA do? Mechanism and stereochemistry of epoxidation.",
     "mCPBA (meta-chloroperoxybenzoic acid) is a peroxyacid that converts alkenes to EPOXIDES.\nMechanism: Concerted \u2014 the peroxyacid delivers an oxygen atom to the alkene in a single step (butterfly mechanism).\nStereochemistry: SYN addition \u2014 the oxygen adds to one face. A cis-alkene gives a cis-epoxide; a trans-alkene gives a trans-epoxide. The stereochemistry of the alkene is RETAINED in the product."),

    ("What is syn-dihydroxylation? Reagent and product?",
     "Reagent: OsO\u2084 (osmium tetroxide), usually with NMO (N-methylmorpholine N-oxide) as a co-oxidant to make OsO\u2084 catalytic.\nReaction: Adds two \u2013OH groups across a double bond.\nStereochemistry: SYN addition \u2014 both OH groups add to the SAME face through a cyclic osmate ester intermediate.\nProduct: cis-1,2-diol (vicinal diol).\nAlternative: KMnO\u2084 (cold, dilute, basic) also gives syn-dihydroxylation but is harder to control."),

    ("What is ozonolysis? Reagents and products?",
     "Reagents: 1. O\u2083 (ozone), 2. Reductive workup: Zn/AcOH or (CH\u2083)\u2082S (dimethyl sulfide). Oxidative workup: H\u2082O\u2082.\nReaction: CLEAVES the C=C double bond completely.\nProducts (reductive workup):\n- Each C of the double bond becomes a C=O.\n- R\u2082C=CR\u2082 \u2192 two ketones\n- RHC=CHR \u2192 two aldehydes\n- R\u2082C=CHR \u2192 one ketone + one aldehyde\n- RCH=CH\u2082 \u2192 aldehyde + formaldehyde (HCHO)\nOxidative workup: Aldehydes \u2192 carboxylic acids.\nUseful for determining alkene structure from fragments."),

    # Oxidation Reactions
    ("What does PCC (pyridinium chlorochromate) do?",
     "PCC (Cr-based oxidant, mild, used in CH\u2082Cl\u2082) selectively oxidizes:\n1\u00b0 alcohol \u2192 ALDEHYDE (stops here \u2014 does NOT overoxidize to carboxylic acid)\n2\u00b0 alcohol \u2192 KETONE\n3\u00b0 alcohol \u2192 NO REACTION\nKey: PCC is the reagent of choice when you need to stop oxidation at the aldehyde stage. It works in anhydrous conditions (CH\u2082Cl\u2082), which prevents overoxidation. Dess-Martin periodinane (DMP) is a modern alternative."),

    ("What does Jones reagent (CrO\u2083/H\u2082SO\u2084/acetone) do?",
     "Jones reagent is a STRONG oxidant:\n1\u00b0 alcohol \u2192 CARBOXYLIC ACID (goes all the way \u2014 oxidizes through aldehyde to acid)\n2\u00b0 alcohol \u2192 KETONE\n3\u00b0 alcohol \u2192 NO REACTION (under normal conditions; harsh conditions can cleave C\u2013C bonds)\nJones reagent works in aqueous acetone. The water present allows overoxidation of the aldehyde intermediate to the carboxylic acid via the hydrate."),

    ("What does KMnO\u2084 do to alkenes under different conditions?",
     "Cold, dilute, basic KMnO\u2084: SYN dihydroxylation \u2192 cis-1,2-diol (with brown MnO\u2082 precipitate). Baeyer test for unsaturation.\nHot, concentrated, acidic KMnO\u2084: OXIDATIVE CLEAVAGE of C=C bond \u2192 carboxylic acids and/or ketones.\n- RHC=CHR \u2192 2 carboxylic acids\n- R\u2082C=CR\u2082 \u2192 2 ketones\n- RCH=CH\u2082 \u2192 RCOOH + CO\u2082 (terminal CH\u2082 fully oxidized)\nSimilar cleavage results to ozonolysis but harsher."),

    # Reduction Reactions
    ("Compare NaBH\u2084 and LiAlH\u2084 as reducing agents: selectivity and conditions.",
     "NaBH\u2084 (sodium borohydride): MILD, SELECTIVE reducing agent.\n- Reduces: aldehydes \u2192 1\u00b0 alcohols, ketones \u2192 2\u00b0 alcohols\n- Does NOT reduce: esters, carboxylic acids, amides, epoxides (usually)\n- Solvent: MeOH, EtOH, or water (tolerates protic solvents)\n\nLiAlH\u2084 (lithium aluminum hydride): POWERFUL, NON-SELECTIVE reducing agent.\n- Reduces: ALL of the above PLUS esters \u2192 1\u00b0 alcohols, carboxylic acids \u2192 1\u00b0 alcohols, amides \u2192 amines, epoxides \u2192 alcohols\n- Solvent: Anhydrous ether or THF ONLY (reacts violently with water/protic solvents)\n- Workup: Aqueous acid quench after reaction"),

    ("What is the selectivity difference between NaBH\u2084 and LiAlH\u2084 for reducing an ester vs a ketone in the same molecule?",
     "NaBH\u2084 will SELECTIVELY reduce the ketone to an alcohol while LEAVING the ester untouched. LiAlH\u2084 will reduce BOTH \u2014 the ketone to a 2\u00b0 alcohol AND the ester to two 1\u00b0 alcohols. This selectivity makes NaBH\u2084 invaluable for chemoselective reductions."),

    # Grignard Reactions
    ("What are Grignard reagents and what do they react with?",
     "Grignard reagent: RMgX (made from R\u2013X + Mg in anhydrous ether or THF). The carbon is a strong NUCLEOPHILE and BASE.\nReactions with carbonyls (add R group, then acid workup gives alcohol):\n- HCHO (formaldehyde) + RMgX \u2192 1\u00b0 alcohol\n- RCHO (aldehyde) + R\u2019MgX \u2192 2\u00b0 alcohol\n- R\u2082CO (ketone) + R\u2019MgX \u2192 3\u00b0 alcohol\n- Ester + 2 eq RMgX \u2192 3\u00b0 alcohol\n- CO\u2082 + RMgX \u2192 carboxylic acid (after acid workup)\n- Epoxide + RMgX \u2192 alcohol (adds 2 carbons, opens at less substituted end)\nCRITICAL: Grignards are destroyed by any acidic proton (H\u2082O, ROH, NH, COOH). Reaction must be ANHYDROUS."),

    ("What is the Grignard reagent incompatibility rule?",
     "Grignard reagents (RMgX) react with ANY acidic hydrogen (pKa < ~45). The molecule being reacted with a Grignard CANNOT contain:\n- \u2013OH (alcohol, phenol)\n- \u2013NH (amine, amide)\n- \u2013SH (thiol)\n- \u2013COOH (carboxylic acid)\n- terminal alkyne C\u2261C\u2013H\nIf these groups are present, they will protonate the Grignard (RMgX + HA \u2192 RH + MgXA) before it can do the desired nucleophilic addition. Protect these groups first or use a different strategy."),

    # Aldol and Condensation
    ("What is the Aldol Reaction / Aldol Condensation?",
     "Aldol reaction: An enolizable aldehyde (or ketone) reacts with base (NaOH) to form an ENOLATE, which then attacks a second aldehyde/ketone carbonyl \u2192 gives a \u03b2-hydroxy aldehyde (or ketone) = aldol product.\nAldol condensation: Upon HEATING, the aldol product undergoes DEHYDRATION (\u2013H\u2082O) \u2192 gives an \u03b1,\u03b2-unsaturated carbonyl (conjugated enone).\nCrossed aldol: Between two different carbonyl compounds \u2014 gives mixtures unless one partner has no \u03b1-hydrogens (e.g., benzaldehyde, formaldehyde) or directed conditions (LDA, kinetic enolate)."),

    # Esterification
    ("What is Fischer Esterification? Reagents, mechanism, and equilibrium.",
     "Reaction: Carboxylic acid + alcohol \u21cc ester + water (acid-catalyzed, REVERSIBLE).\nCatalyst: H\u2082SO\u2084 or HCl (acid catalyst).\nMechanism:\n1. Protonation of carbonyl oxygen\n2. Nucleophilic attack of alcohol on protonated carbonyl\n3. Proton transfer\n4. Loss of water (leaving group)\n5. Deprotonation \u2192 ester product\nKey: REVERSIBLE (equilibrium). Drive forward by: excess alcohol, removing water (Dean-Stark trap), or excess acid. Uses acid catalyst \u2014 no strong nucleophiles or bases involved."),

    # Hydrolysis
    ("Compare acid-catalyzed vs base-catalyzed hydrolysis of esters.",
     "ACID-CATALYZED (reverse of Fischer esterification):\nEster + H\u2082O + H\u207a catalyst \u21cc carboxylic acid + alcohol. REVERSIBLE.\n\nBASE-CATALYZED (saponification):\nEster + NaOH \u2192 carboxylate salt (RCOO\u207bNa\u207a) + alcohol. IRREVERSIBLE.\nWhy irreversible? The carboxylate anion (resonance-stabilized) is a very poor electrophile \u2014 the reverse reaction doesn\u2019t occur. This is why saponification goes to completion.\nSaponification of fats (triesters of glycerol) produces SOAP (carboxylate salts) + glycerol."),

    # Electrophilic Aromatic Substitution
    ("What is the general mechanism for Electrophilic Aromatic Substitution (EAS)?",
     "Step 1: Generation of the electrophile (E\u207a).\nStep 2: Electrophilic attack \u2014 \u03c0 electrons of benzene attack E\u207a \u2192 form ARENIUM ION (sigma complex/Wheland intermediate). This is a resonance-stabilized carbocation (3 resonance structures). This is the RATE-DETERMINING STEP.\nStep 3: Deprotonation \u2014 a base removes H\u207a from the sp\u00b3 carbon \u2192 restores aromaticity.\nKey: SUBSTITUTION not addition \u2014 aromaticity is preserved. The aromatic ring acts as a nucleophile."),

    ("What are the reagents for bromination of benzene (EAS)?",
     "Reagents: Br\u2082 + FeBr\u2083 (Lewis acid catalyst).\nMechanism: FeBr\u2083 polarizes Br\u2082 \u2192 generates electrophilic Br\u207a (or Br\u2013Br\u2013FeBr\u2083 complex). Benzene attacks Br\u207a \u2192 arenium ion \u2192 deprotonation \u2192 bromobenzene + HBr.\nFeBr\u2083 is regenerated. AlBr\u2083 also works as the Lewis acid.\nNote: Without Lewis acid catalyst, Br\u2082 does NOT react with benzene (not electrophilic enough). Exception: activated rings like phenol or aniline react with Br\u2082/H\u2082O without catalyst."),

    ("What are the reagents for nitration of benzene (EAS)?",
     "Reagents: HNO\u2083 + H\u2082SO\u2084 (mixed acid).\nElectrophile generated: NO\u2082\u207a (nitronium ion), formed by protonation and dehydration of HNO\u2083 by H\u2082SO\u2084.\nProduct: Nitrobenzene.\nThe nitro group is a strong deactivating, meta-directing group \u2014 so further nitration is slower and gives m-dinitrobenzene."),

    ("What are Friedel-Crafts Alkylation and Acylation?",
     "ALKYLATION: ArH + RCl + AlCl\u2083 \u2192 ArR + HCl\nElectrophile: R\u207a carbocation (generated from RCl + AlCl\u2083). Problem: Carbocation can rearrange (1\u00b0 \u2192 2\u00b0 \u2192 3\u00b0). Also, product is MORE reactive than starting material \u2192 polyalkylation.\n\nACYLATION: ArH + RCOCl + AlCl\u2083 \u2192 ArCOR + HCl\nElectrophile: Acylium ion (RC\u2261O\u207a, resonance-stabilized \u2014 NO rearrangement). Product ketone is deactivated \u2192 NO polyacylation.\nLimitation: Neither reaction works on strongly deactivated rings (\u2013NO\u2082, \u2013CF\u2083, \u2013COR, \u2013SO\u2083H, \u2013NR\u2083\u207a)."),

    ("What are activating and deactivating groups in EAS? What are the directing effects?",
     "ACTIVATING (make ring MORE reactive than benzene, donate electron density):\n- Strong activating (ortho/para directors): \u2013NH\u2082, \u2013NHR, \u2013NR\u2082, \u2013OH, \u2013OR\n- Moderate activating (ortho/para): \u2013NHCOR, \u2013OCOR\n- Weak activating (ortho/para): \u2013CH\u2083, \u2013R (alkyl groups \u2014 hyperconjugation/induction)\n\nDEACTIVATING (make ring LESS reactive):\n- Weak deactivating (ortho/para director!): \u2013F, \u2013Cl, \u2013Br, \u2013I (halogens \u2014 special case!)\n- Moderate/strong deactivating (META directors): \u2013NO\u2082, \u2013CN, \u2013SO\u2083H, \u2013COR, \u2013COOR, \u2013COOH, \u2013CF\u2083, \u2013NR\u2083\u207a\n\nKey exception: Halogens are deactivating but ortho/para directing (inductive withdrawal but lone pair donation by resonance)."),

    ("Why are halogens ortho/para directors but deactivating?",
     "Two competing effects:\n1. INDUCTIVE EFFECT: Halogens are electronegative \u2192 withdraw electron density through \u03c3 bonds \u2192 deactivating (makes ring less electron-rich overall \u2192 slower reaction than benzene).\n2. RESONANCE EFFECT: Lone pairs on halogen can donate into the ring by resonance \u2192 stabilizes the arenium ion intermediate ONLY for ortho/para attack (not meta).\nThe inductive effect dominates for RATE (deactivating), but resonance dominates for REGIOCHEMISTRY (ortho/para directing). Net result: slower than benzene, but substitution occurs at ortho/para positions."),

    # Radical Reactions
    ("Describe the mechanism of radical halogenation of alkanes.",
     "Three stages:\n\nINITIATION: Homolytic cleavage of X\u2082 by heat (\u0394) or light (h\u03bd) \u2192 2 X\u2022 radicals.\n\nPROPAGATION (chain-carrying):\nStep 1: X\u2022 + R\u2013H \u2192 HX + R\u2022 (H abstraction). Rate-determining step.\nStep 2: R\u2022 + X\u2082 \u2192 R\u2013X + X\u2022 (halogen transfer). Regenerates X\u2022.\n\nTERMINATION (any two radicals combine):\nR\u2022 + R\u2022 \u2192 R\u2013R\nR\u2022 + X\u2022 \u2192 R\u2013X\nX\u2022 + X\u2022 \u2192 X\u2082\n\nSelectivity: Br\u2022 is MORE selective than Cl\u2022 (Br\u2022 preferentially abstracts 3\u00b0 > 2\u00b0 > 1\u00b0 H). Hammond postulate: Br\u2022 abstraction is endothermic with late TS \u2192 more selective."),

    ("What is the selectivity of radical bromination vs chlorination?",
     "CHLORINATION: Relatively NON-selective.\nRelative reactivity: 3\u00b0:2\u00b0:1\u00b0 \u2248 5:4:1\nGives mixtures of products. Useful mainly for methane \u2192 CH\u2083Cl.\n\nBROMINATION: Highly SELECTIVE.\nRelative reactivity: 3\u00b0:2\u00b0:1\u00b0 \u2248 1600:80:1\nAlmost exclusively reacts at the most substituted position (most stable radical).\nReason (Hammond Postulate): H-abstraction by Br\u2022 is endothermic \u2192 late, product-like transition state \u2192 TS stability reflects radical stability \u2192 high selectivity."),

    # Key Reagent Cards
    ("What does Br\u2082 / FeBr\u2083 do?",
     "Electrophilic aromatic substitution (EAS): Bromination of benzene ring. Adds \u2013Br to aromatic ring. Requires Lewis acid catalyst (FeBr\u2083 or AlBr\u2083) for unactivated rings. Activated rings (phenol, aniline) react with Br\u2082/H\u2082O without catalyst."),

    ("What does Br\u2082 / CCl\u2084 (or CH\u2082Cl\u2082) do?",
     "Halogenation of alkenes: ANTI addition of Br\u2082 across C=C double bond via bromonium ion intermediate \u2192 vicinal dibromide (1,2-dibromide). Also a qualitative test for unsaturation \u2014 orange Br\u2082 solution decolorizes."),

    ("What does HBr alone vs HBr/ROOR do?",
     "HBr alone: Markovnikov addition to alkene. H adds to less substituted C, Br to more substituted C. Mechanism: electrophilic addition via carbocation.\nHBr/ROOR (peroxides): ANTI-Markovnikov addition. Br adds to less substituted C, H to more substituted C. Mechanism: radical chain. Note: This only works with HBr \u2014 HCl and HI do not undergo radical addition (thermodynamic reasons)."),

    ("What does BH\u2083\u00b7THF followed by H\u2082O\u2082/NaOH do?",
     "Hydroboration-oxidation: Anti-Markovnikov, SYN addition of H\u2082O across alkene.\nStep 1: BH\u2083 adds to less substituted carbon (concerted, syn addition \u2014 B and H add to same face).\nStep 2: H\u2082O\u2082/NaOH oxidizes C\u2013B bond \u2192 C\u2013OH with retention of configuration.\nOverall: Produces the anti-Markovnikov alcohol with syn stereochemistry. Complementary to acid-catalyzed hydration (which gives Markovnikov product)."),

    ("What does H\u2082/Pd(C) do? What about H\u2082/Lindlar\u2019s catalyst?",
     "H\u2082/Pd(C): Catalytic hydrogenation. Reduces C=C to C\u2013C (syn addition). Reduces C\u2261C to C\u2013C (fully). Also removes Bn (benzyl) protecting groups. Does NOT reduce C=O in most cases.\n\nH\u2082/Lindlar\u2019s catalyst (Pd/CaCO\u2083 + quinoline poison): PARTIAL reduction of alkyne \u2192 CIS alkene (stops at alkene stage because poisoned catalyst). Syn addition gives Z-alkene.\n\nFor trans alkene from alkyne: Use Na/NH\u2083(l) (dissolving metal reduction) \u2192 TRANS (E) alkene via radical anion mechanism."),

    ("What does OsO\u2084 (catalytic) / NMO do?",
     "Syn-dihydroxylation of alkenes \u2192 cis-1,2-diol (vicinal diol). OsO\u2084 forms a cyclic osmate ester (syn addition), then NMO (co-oxidant) reoxidizes Os(VI) back to Os(VIII) making it catalytic. Hydrolysis gives the cis-diol. Stereochemistry: SYN \u2014 both OH groups on same face."),

    ("What does O\u2083 followed by Zn/AcOH (or DMS) do?",
     "Ozonolysis with reductive workup: Cleaves C=C double bond completely \u2192 produces aldehydes and/or ketones.\n- Disubstituted end \u2192 ketone\n- Monosubstituted end \u2192 aldehyde\n- Unsubstituted end (=CH\u2082) \u2192 formaldehyde (HCHO)\nThe Zn/AcOH or (CH\u2083)\u2082S prevents overoxidation of aldehydes to carboxylic acids. If oxidative workup (H\u2082O\u2082) used instead, aldehydes \u2192 carboxylic acids."),

    ("What does PCC (pyridinium chlorochromate) in CH\u2082Cl\u2082 do?",
     "MILD oxidation:\n1\u00b0 alcohol \u2192 aldehyde (STOPS here \u2014 key feature)\n2\u00b0 alcohol \u2192 ketone\n3\u00b0 alcohol \u2192 no reaction\nMust use anhydrous conditions (CH\u2082Cl\u2082 solvent). The absence of water prevents further oxidation of the aldehyde to carboxylic acid. Alternatives with same selectivity: Dess-Martin periodinane (DMP), Swern oxidation."),

    ("What does NaBH\u2084 in MeOH do?",
     "Mild, selective REDUCTION:\n- Aldehyde \u2192 1\u00b0 alcohol\n- Ketone \u2192 2\u00b0 alcohol\nDoes NOT reduce: esters, carboxylic acids, amides, alkenes.\nSafe to use in protic solvents (MeOH, EtOH). Delivers H\u207b (hydride) to electrophilic carbonyl carbon. Workup: aqueous acid."),

    ("What does LiAlH\u2084 in THF do?",
     "Powerful, non-selective REDUCTION:\n- Aldehyde \u2192 1\u00b0 alcohol\n- Ketone \u2192 2\u00b0 alcohol\n- Ester \u2192 1\u00b0 alcohol (+ alcohol from OR\u2019 group)\n- Carboxylic acid \u2192 1\u00b0 alcohol\n- Amide \u2192 amine\n- Epoxide \u2192 alcohol (at less hindered carbon)\nMUST use anhydrous solvent (THF or ether). Reacts violently with water and protic solvents. Workup: careful aqueous quench (e.g., 1. H\u2082O, 2. NaOH, 3. H\u2082O \u2014 Fieser workup)."),

    ("What does RMgBr (Grignard) + carbonyl, then H\u2083O\u207a workup give?",
     "Nucleophilic addition of R group to carbonyl carbon \u2192 new C\u2013C bond:\n- RMgBr + HCHO \u2192 1\u00b0 alcohol (one more carbon)\n- RMgBr + R\u2019CHO \u2192 2\u00b0 alcohol\n- RMgBr + R\u2019\u2082CO \u2192 3\u00b0 alcohol\n- RMgBr + ester \u2192 3\u00b0 alcohol (2 equivalents of RMgBr add)\n- RMgBr + CO\u2082 \u2192 carboxylic acid (after H\u2083O\u207a workup)\n- RMgBr + ethylene oxide \u2192 1\u00b0 alcohol with 2 extra carbons\nREQUIRES absolutely anhydrous conditions."),

    ("What does SOCl\u2082 (thionyl chloride) do to alcohols and carboxylic acids?",
     "With alcohol: R\u2013OH + SOCl\u2082 \u2192 R\u2013Cl + SO\u2082\u2191 + HCl\u2191\nConverts alcohol to alkyl chloride. Good leaving groups (SO\u2082 and HCl are gases \u2014 drive reaction forward). Retention or inversion depending on mechanism (SNi for some, SN2 with added base).\nWith carboxylic acid: RCOOH + SOCl\u2082 \u2192 RCOCl + SO\u2082 + HCl\nConverts carboxylic acid to acid chloride (acyl chloride). Essential for making reactive acyl derivatives."),

    ("What does H\u2082SO\u2084 (concentrated) at high temperature do to alcohols?",
     "DEHYDRATION of alcohols \u2192 alkenes (elimination).\nConditions: Concentrated H\u2082SO\u2084, high temperature (typically 180\u00b0C for 1\u00b0 alcohols, lower for 2\u00b0 and 3\u00b0).\nMechanism: E1 for 3\u00b0 and 2\u00b0 alcohols (via carbocation). E2 for 1\u00b0 alcohols.\nRegiochemistry: Zaitsev product (most substituted alkene) is major product.\nCarbocation rearrangements possible (1,2-hydride or methyl shifts for 2\u00b0 and 3\u00b0)."),

    ("What does NaOH/H\u2082O (aqueous base) do to acid chlorides, anhydrides, and esters?",
     "Nucleophilic acyl substitution \u2014 hydrolysis:\n- Acid chloride + NaOH \u2192 carboxylate salt + Cl\u207b (fast, irreversible)\n- Anhydride + NaOH \u2192 2 carboxylate salts (fast)\n- Ester + NaOH \u2192 carboxylate salt + alcohol (saponification, irreversible because carboxylate is stabilized)\nReactivity order: acid chloride > anhydride > ester > amide. The better the leaving group, the more reactive the acyl derivative."),

    ("What does Na/NH\u2083(l) \u2014 dissolving metal reduction \u2014 do to alkynes?",
     "Reduces internal alkynes to TRANS (E) alkenes. Mechanism: Radical anion pathway \u2014 Na donates electrons to the alkyne \u2192 vinyl radical anion \u2192 protonation by NH\u2083 \u2192 vinyl radical \u2192 second electron from Na \u2192 vinyl anion \u2192 second protonation \u2192 trans-alkene. The trans selectivity arises because the more stable trans-vinyl anion is formed preferentially. Complementary to Lindlar (which gives cis)."),

    ("What does mCPBA do to alkenes?",
     "Epoxidation: Converts alkene to an epoxide (oxirane). Concerted mechanism \u2014 stereochemistry of the alkene is preserved (cis-alkene \u2192 cis-epoxide, trans-alkene \u2192 trans-epoxide). The oxygen is delivered from the peroxyacid to ONE face of the alkene (syn). Alternative epoxidation reagents: DMDO, Sharpless asymmetric epoxidation (with chiral Ti catalyst for enantioselective)."),

    # CORRECTION APPLIED: (RCO)₂O instead of RCO₂COR
    ("Rank the reactivity of carboxylic acid derivatives toward nucleophilic acyl substitution.",
     "Most reactive \u2192 least reactive:\nAcid chloride (RCOCl) > Acid anhydride ((RCO)\u2082O) > Ester (RCOOR\u2019) > Amide (RCONR\u2082) > Carboxylate (RCOO\u207b)\n\nReasoning: Reactivity depends on leaving group ability AND resonance donation to carbonyl:\n- Cl\u207b is a good LG, minimal resonance donation \u2192 most reactive\n- Carboxylate (RCOO\u207b) is a moderate LG\n- OR is a moderate LG, moderate resonance\n- NR\u2082 is a poor LG, strong resonance donation \u2192 least reactive\n- O\u207b is a terrible LG \u2192 carboxylates are unreactive\nYou can go DOWN the series (more reactive \u2192 less reactive) but NOT up without special activation."),
]

# ─── DECK 3: Stereochemistry & Spectroscopy (40 cards) ───
SPECTROSCOPY_CARDS = [
    # Chirality Basics
    ("What is a CHIRAL molecule? How do you identify a chiral center?",
     "A chiral molecule is non-superimposable on its mirror image. A CHIRAL CENTER (stereocenter) is typically a carbon with FOUR DIFFERENT substituents (sp\u00b3, tetrahedral geometry). To identify: check each sp\u00b3 carbon \u2014 does it have 4 different groups? If yes, it\u2019s a stereocenter. A molecule can be chiral without a stereocenter (e.g., allenes, biaryls) but this is less common."),

    ("How do you assign R or S configuration using Cahn-Ingold-Prelog (CIP) rules?",
     "Step 1: Assign PRIORITY to the 4 substituents by atomic number (higher atomic number = higher priority). Rank 1 (highest) to 4 (lowest).\nStep 2: If tied at first atom, go outward to the next atom of difference (first point of difference wins).\nStep 3: Orient the molecule so priority #4 points AWAY from you (into the page).\nStep 4: Trace a path from 1\u21922\u21923. CLOCKWISE = R (rectus). COUNTERCLOCKWISE = S (sinister).\nTie-breakers: Double bond = two single bonds to that atom (phantom duplicate atoms)."),

    ("What are CIP priority rules for common atoms and groups?",
     "By atomic number: I(53) > Br(35) > Cl(17) > S(16) > O(8) > N(7) > C(6) > H(1).\nCommon group priorities (high to low): \u2013I > \u2013Br > \u2013Cl > \u2013OH > \u2013NH\u2082 > \u2013COOH > \u2013CHO > \u2013CH\u2082OH > \u2013C\u2086H\u2085 > \u2013C\u2261CH > \u2013CH=CH\u2082 > \u2013CH\u2082CH\u2083 > \u2013CH\u2083 > \u2013H\nMultiple bonds: C=O counts as C bonded to O,O (two phantom O atoms). C\u2261C counts as C bonded to C,C,C."),

    # Enantiomers
    ("What are ENANTIOMERS? What properties do they share and how do they differ?",
     "Enantiomers: Non-superimposable mirror images. They have OPPOSITE R/S configurations at ALL stereocenters.\nSAME properties: melting point, boiling point, solubility, Rf value, IR spectrum, NMR spectrum, density \u2014 identical in achiral environments.\nDIFFERENT properties: Optical rotation (equal magnitude, opposite sign: one is +, other is \u2013), behavior with chiral reagents/enzymes/receptors, and retention time on chiral HPLC columns."),

    ("What is optical activity? What is specific rotation?",
     "Optical activity: The ability of chiral compounds to rotate plane-polarized light. Measured with a polarimeter.\nDextrorotatory (+) or (d): Rotates light clockwise.\nLevorotatory (\u2013) or (l): Rotates light counterclockwise.\nSpecific rotation: [\u03b1]_D = \u03b1/(c \u00d7 l) where \u03b1 = observed rotation (degrees), c = concentration (g/mL), l = path length (dm).\nIMPORTANT: (+)/(\u2013) designation has NO correlation to R/S configuration. Must be determined experimentally."),

    # Diastereomers
    ("What are DIASTEREOMERS? How do their properties compare?",
     "Diastereomers: Stereoisomers that are NOT mirror images. They have the same connectivity but differ in configuration at ONE OR MORE (but not all) stereocenters.\nProperties: DIFFERENT melting point, boiling point, solubility, Rf, NMR, specific rotation \u2014 they are different compounds with different physical and chemical properties.\nExamples: cis/trans isomers, (2R,3R) vs (2R,3S) tartaric acid. Maximum stereoisomers for n stereocenters = 2\u207f (but may be fewer if meso forms exist)."),

    # Meso Compounds
    ("What is a MESO compound? How do you identify one?",
     "A meso compound has chiral centers but is ACHIRAL overall because it possesses an INTERNAL MIRROR PLANE (plane of symmetry).\nIdentification: Look for a molecule with 2+ stereocenters where one half is the mirror image of the other half. The stereocenters have opposite configurations (one R, one S) that cancel out.\nExample: (2R,3S)-tartaric acid \u2014 has two chiral centers but an internal mirror plane \u2192 achiral, optically inactive.\nMeso compounds are NOT optically active (specific rotation = 0). They reduce the expected 2\u207f stereoisomers."),

    # Racemic Mixture
    ("What is a RACEMIC MIXTURE? Properties?",
     "A racemic mixture (racemate, \u00b1, dl, or rac): A 50:50 mixture of two enantiomers.\nProperties:\n- Optically INACTIVE (rotations cancel: [\u03b1] = 0)\n- May have different melting point than pure enantiomer (racemic crystals pack differently)\n- Labeled as (\u00b1) or rac-\nResolution: Separating a racemic mixture into pure enantiomers. Methods: chiral HPLC, diastereomeric salt formation, enzymatic resolution."),

    # Fischer Projections
    ("How do you draw and interpret FISCHER PROJECTIONS?",
     "Convention: Carbon chain is drawn vertically with C1 (most oxidized carbon) at TOP.\n- HORIZONTAL lines = bonds coming TOWARD you (out of page, wedges)\n- VERTICAL lines = bonds going AWAY from you (into page, dashes)\nRules for manipulation:\n1. Can rotate 180\u00b0 in the plane (still same molecule)\n2. CANNOT rotate 90\u00b0 (changes configuration!)\n3. Can swap any two groups \u2014 one swap = enantiomer, two swaps = same molecule\nTo determine R/S: If lowest priority group is on a vertical line (going back), read 1\u21922\u21923 directly. If on horizontal (coming forward), the answer is OPPOSITE of what you read."),

    # Newman Projections
    ("How do you draw NEWMAN PROJECTIONS? What do anti and gauche mean?",
     "View the molecule along a C\u2013C bond axis. Front carbon = dot (intersection of 3 bonds). Back carbon = circle.\n- STAGGERED conformations: Bonds on front and back are offset (60\u00b0 dihedral). Lower energy.\n- ECLIPSED conformations: Bonds align (0\u00b0 dihedral). Higher energy (torsional strain).\n\nFor butane along C2\u2013C3:\n- ANTI: Two largest groups (methyls) are 180\u00b0 apart. LOWEST energy staggered conformation.\n- GAUCHE: Two largest groups are 60\u00b0 apart. Higher energy than anti by ~0.9 kcal/mol (steric strain) but still staggered.\n- Eclipsed: Highest energy. Totally eclipsed (methyls at 0\u00b0) is the global maximum."),

    ("What types of strain affect conformational energy?",
     "1. TORSIONAL STRAIN (Pitzer strain): Resistance to bond eclipsing. Results from electron repulsion in eclipsed bonds. Even H/H eclipsing costs ~1 kcal/mol.\n2. STERIC STRAIN (van der Waals strain): Repulsion between electron clouds of bulky groups that are too close. Gauche butane interaction \u2248 0.9 kcal/mol.\n3. ANGLE STRAIN (Baeyer strain): Deviation from ideal bond angles (109.5\u00b0 for sp\u00b3). Significant in small rings: cyclopropane (60\u00b0, very strained), cyclobutane (90\u00b0, strained), cyclopentane (108\u00b0, nearly ideal)."),

    # Ring Conformations
    ("Describe CHAIR CONFORMATION of cyclohexane: axial vs equatorial positions.",
     "Cyclohexane adopts a chair conformation to minimize strain (all angles \u2248 111\u00b0, all H\u2019s staggered).\nEach carbon has one AXIAL position (pointing straight up or down, parallel to ring axis) and one EQUATORIAL position (pointing outward, roughly in the plane).\nAlternating pattern: If one carbon has axial-up, the adjacent carbon has axial-down.\n6 axial + 6 equatorial = 12 total H positions.\nRing flip: Converts all axial to equatorial and vice versa. Axial-up becomes equatorial-down and vice versa."),

    ("What are 1,3-DIAXIAL INTERACTIONS? Why do substituents prefer equatorial?",
     "1,3-Diaxial interactions: Steric repulsion between an AXIAL substituent and the two axial hydrogens (or groups) on the same face of the ring, located on C3 and C5 (1,3-relationship). Analogous to gauche interactions in Newman projections.\nEquatorial preference: Equatorial substituents point outward and avoid these 1,3-diaxial interactions. Larger groups have stronger equatorial preference:\n- \u2013CH\u2083: 1.7 kcal/mol (equatorial favored)\n- \u2013CH\u2082CH\u2083: 1.8 kcal/mol\n- \u2013C(CH\u2083)\u2083 (t-butyl): 4.9 kcal/mol (essentially locks the ring)\n- \u2013OH: 0.9 kcal/mol\n- \u2013F: 0.3 kcal/mol"),

    ("How do you analyze a DISUBSTITUTED cyclohexane chair conformation?",
     "1. Draw both chair conformations (ring flip interconverts them).\n2. Place substituents: In one chair, determine if each is axial or equatorial.\n3. Ring flip: Axial becomes equatorial and vice versa.\n4. The MORE STABLE chair has the LARGER group EQUATORIAL.\n5. If both groups are on the same carbon: gem-disubstituted.\n6. Trans-1,2: one axial + one equatorial in BOTH chairs (diequatorial exists in one chair).\n7. Cis-1,2: both axial or both equatorial.\nRemember: cis = same side of ring plane, trans = opposite sides."),

    ("What is a BOAT conformation? How does it compare to a chair?",
     "The boat conformation is an alternative non-planar conformation of cyclohexane. It is ~7 kcal/mol HIGHER in energy than the chair due to:\n1. FLAGPOLE interactions: H\u2019s on C1 and C4 point inward and clash sterically (like the bow and stern of a boat).\n2. ECLIPSING strain: 4 pairs of eclipsed C\u2013H bonds along the sides.\nThe twist-boat is slightly more stable than the true boat (~1.5 kcal/mol lower) because it partially relieves flagpole and eclipsing interactions. The chair is still the most stable by far."),

    # E/Z Nomenclature
    ("How do you assign E/Z configuration to alkenes?",
     "Step 1: For each carbon of the C=C, identify the two substituents and assign CIP priorities (higher atomic number = higher priority).\nStep 2: Compare the positions of the HIGHER-priority group on each carbon:\n- Z (zusammen, \u2018together\u2019): Higher-priority groups on the SAME side of the double bond.\n- E (entgegen, \u2018opposite\u2019): Higher-priority groups on OPPOSITE sides.\nCis/trans only works for 2 groups total; E/Z works for ALL alkenes (even tri- and tetrasubstituted)."),

    ("When does cis/trans NOT equal Z/E?",
     "cis/trans and Z/E can disagree when priority assignments differ from visual \u2018same side\u2019 assessment.\nExample: 1-bromo-2-chloroethene. Br and Cl on the same side = cis visually, but CIP priority: on C1, Br > H; on C2, Cl > H. Both higher-priority groups (Br and Cl) are on the same side \u2192 Z. Here cis = Z.\nBUT: In (Z)-1-bromo-1-chloro-2-methylpropene, visual \u2018cis\u2019 may not match Z if you track the wrong groups. ALWAYS use CIP priorities, not visual intuition."),

    # IR Spectroscopy
    ("What are the KEY IR absorptions every organic chemistry student must know?",
     "O\u2013H (alcohol): 3200\u20133600 cm\u207b\u00b9, BROAD\nO\u2013H (carboxylic acid): 2500\u20133300 cm\u207b\u00b9, VERY BROAD (overlaps C\u2013H region)\nN\u2013H (amine): 3300\u20133500 cm\u207b\u00b9, MEDIUM (1\u00b0 amine: 2 peaks, 2\u00b0 amine: 1 peak)\nC\u2013H (sp\u00b3): 2850\u20133000 cm\u207b\u00b9\nC\u2013H (sp\u00b2): 3000\u20133100 cm\u207b\u00b9\nC\u2013H (sp, alkyne): ~3300 cm\u207b\u00b9, SHARP\nC\u2261N (nitrile): ~2200 cm\u207b\u00b9, SHARP\nC\u2261C (alkyne): ~2150 cm\u207b\u00b9, SHARP (may be absent if internal & symmetric)\nC=O (carbonyl): ~1700 cm\u207b\u00b9, STRONG and SHARP (most diagnostic peak in IR)\nC=C (alkene): ~1650 cm\u207b\u00b9, MEDIUM"),

    # CORRECTION APPLIED: 2720 and 2820 cm⁻¹ (not 2850)
    ("How do you distinguish between different carbonyl compounds using IR C=O stretch position?",
     "C=O stretch position varies by functional group:\n- Acid chloride: ~1800 cm\u207b\u00b9\n- Acid anhydride: ~1800 and ~1750 cm\u207b\u00b9 (TWO C=O peaks!)\n- Ester: ~1735\u20131750 cm\u207b\u00b9\n- Aldehyde: ~1720\u20131740 cm\u207b\u00b9 (also has 2 C\u2013H stretches at 2720 and 2820 cm\u207b\u00b9 \u2014 Fermi resonance doublet)\n- Ketone: ~1705\u20131720 cm\u207b\u00b9\n- Carboxylic acid: ~1710 cm\u207b\u00b9 (plus very broad O\u2013H)\n- Amide: ~1630\u20131690 cm\u207b\u00b9 (lower due to strong N resonance donation)\nConjugation LOWERS the C=O frequency. Ring strain RAISES it."),

    ("How do you distinguish an alcohol, carboxylic acid, and amine using IR?",
     "ALCOHOL: Broad O\u2013H stretch at 3200\u20133600 cm\u207b\u00b9. NO carbonyl peak near 1700 cm\u207b\u00b9.\nCARBOXYLIC ACID: VERY broad O\u2013H stretch from 2500\u20133300 cm\u207b\u00b9 (so broad it overlaps C\u2013H region \u2014 distinctive \u2018haystack\u2019 shape). PLUS strong C=O at ~1710 cm\u207b\u00b9.\nAMINE: N\u2013H stretch at 3300\u20133500 cm\u207b\u00b9. 1\u00b0 amine shows TWO peaks (symmetric and asymmetric N\u2013H stretch). 2\u00b0 amine shows ONE peak. 3\u00b0 amine shows NO N\u2013H peak. Also look for C\u2013N stretch at 1020\u20131250 cm\u207b\u00b9."),

    # NMR Spectroscopy
    ("What are the basics of \u00b9H NMR? What information does a spectrum provide?",
     "\u00b9H NMR provides 4 types of information:\n1. CHEMICAL SHIFT (\u03b4, ppm): Position of signal \u2014 indicates electronic environment (shielded vs deshielded).\n2. INTEGRATION: Area under peak \u2014 proportional to NUMBER of H\u2019s giving that signal.\n3. SPLITTING PATTERN: Multiplicity (n+1 rule) \u2014 tells you how many H\u2019s are on adjacent carbons.\n4. NUMBER OF SIGNALS: Tells you how many chemically distinct types of H\u2019s exist.\nEquivalent protons give ONE signal. Symmetry reduces the number of signals."),

    ("What are the common \u00b9H NMR chemical shift ranges?",
     "TMS (reference): 0.0 ppm\nAlkyl (R\u2013CH\u2083, R\u2082CH\u2082): 0.8\u20131.5 ppm\nAllylic (C=C\u2013CH): 1.5\u20132.5 ppm\n\u03b1 to C=O (O=C\u2013CH): 2.0\u20132.5 ppm\nN\u2013CH: 2.2\u20132.9 ppm\nO\u2013CH (ether, alcohol): 3.3\u20134.0 ppm\nVinylic (C=C\u2013H): 4.5\u20136.5 ppm\nAromatic (Ar\u2013H): 6.5\u20138.0 ppm\nAldehyde (RCHO): 9.0\u201310.0 ppm\nCarboxylic acid (RCOOH): 10\u201312 ppm (broad, exchangeable)\nAlcohol (R\u2013OH): 1\u20135 ppm (variable, exchangeable, often broad)\nAmine (R\u2013NH): 0.5\u20133 ppm (variable, exchangeable)"),

    ("Explain the N+1 RULE for splitting patterns in \u00b9H NMR.",
     "The n+1 rule: A proton with n equivalent neighboring protons (on adjacent carbons) is split into (n+1) peaks.\nMultiplicities:\n0 neighbors \u2192 singlet (s)\n1 neighbor \u2192 doublet (d)\n2 neighbors \u2192 triplet (t)\n3 neighbors \u2192 quartet (q)\n4 neighbors \u2192 quintet\n5 neighbors \u2192 sextet\n6 neighbors \u2192 septet (heptet)\nIntensity ratios follow Pascal\u2019s triangle (e.g., triplet = 1:2:1, quartet = 1:3:3:1).\nProtons split EACH OTHER (coupling is mutual). Equivalent protons do NOT split each other. OH and NH protons usually appear as broad singlets (rapid exchange)."),

    ("What is COUPLING CONSTANT (J value) in NMR and what does it tell you?",
     "Coupling constant (J): The distance in Hz between peaks in a multiplet. Mutually coupled protons have the SAME J value.\nTypical J values:\n- Geminal (2-bond, \u00b2J): 0\u201312 Hz\n- Vicinal (3-bond, \u00b3J): 6\u20138 Hz (typical), depends on dihedral angle (Karplus equation)\n- Trans-alkene: \u00b3J = 12\u201318 Hz\n- Cis-alkene: \u00b3J = 6\u201312 Hz\n- Aromatic (ortho): \u00b3J = 6\u201310 Hz\n- Long-range (4+ bonds): Usually 0\u20133 Hz\nJ values help distinguish cis vs trans alkenes and confirm connectivity."),

    ("How do you identify an aldehyde, carboxylic acid, and aromatic compound by \u00b9H NMR?",
     "ALDEHYDE: Signal at \u03b4 9.0\u201310.0 ppm (distinctive downfield singlet or doublet if \u03b1-H present). Only 1H.\nCARBOXYLIC ACID: Very broad signal at \u03b4 10\u201312 ppm (exchangeable, disappears with D\u2082O shake).\nAROMATIC: Signals at \u03b4 6.5\u20138.0 ppm. Integration indicates number of aromatic H\u2019s. Monosubstituted benzene: 5 ArH. Para-disubstituted: 4 ArH showing characteristic two doublets (AA\u2019BB\u2019 pattern)."),

    ("What is a D\u2082O SHAKE in NMR and what does it reveal?",
     "D\u2082O shake: Add D\u2082O to the NMR sample. Exchangeable protons (O\u2013H, N\u2013H, S\u2013H) are replaced by deuterium (D). Since deuterium is NMR-invisible in a \u00b9H experiment, those peaks DISAPPEAR from the spectrum.\nUse: Confirms which peaks are from OH, NH, or COOH groups. If a peak disappears after D\u2082O shake, it\u2019s an exchangeable proton. This helps distinguish between overlapping peaks in the 1\u20135 ppm region (where OH can appear)."),

    # Mass Spectrometry
    ("What information does MASS SPECTROMETRY provide?",
     "1. MOLECULAR ION (M\u207a): The highest significant m/z peak = molecular weight of the compound. Also called the parent ion.\n2. BASE PEAK: The tallest (most abundant) peak in the spectrum. Not necessarily M\u207a.\n3. FRAGMENTATION PATTERN: How the molecule breaks apart \u2192 reveals structural information.\n4. NITROGEN RULE: Odd molecular weight \u2192 odd number of nitrogen atoms. Even MW \u2192 zero or even number of N.\n5. Isotope patterns: Br (M and M+2 in ~1:1 ratio), Cl (M and M+2 in ~3:1 ratio) are diagnostic."),

    ("What are common FRAGMENTATION PATTERNS in mass spectrometry?",
     "Common fragmentations (loss of fragments from M\u207a):\n- Loss of 15 \u2192 loss of CH\u2083 (methyl)\n- Loss of 17 \u2192 loss of OH\n- Loss of 18 \u2192 loss of H\u2082O (alcohols)\n- Loss of 28 \u2192 loss of CO (aldehydes, ketones) or C\u2082H\u2084 (ethylene)\n- Loss of 29 \u2192 loss of CHO (aldehyde) or C\u2082H\u2085\n- Loss of 31 \u2192 loss of OCH\u2083 (methyl ester/methyl ether)\n- Loss of 45 \u2192 loss of OC\u2082H\u2085 (ethyl ester)\n- McLafferty rearrangement: Carbonyls with a \u03b3-hydrogen \u2192 loss of alkene, gives m/z = enol fragment.\n\u03b1-Cleavage next to carbonyl is very common in ketones and aldehydes."),

    ("How do you use the NITROGEN RULE and isotope patterns in mass spectrometry?",
     "NITROGEN RULE: Organic compounds with an ODD molecular weight contain an ODD number of nitrogen atoms (1, 3, 5...). Even MW \u2192 0 or even number of N.\nReason: N has odd valence (3) and even atomic weight (14).\n\nISOTOPE PATTERNS:\n- Bromine: M and M+2 peaks in approximately 1:1 ratio (\u2079Br and \u2078\u00b9Br are nearly equal abundance).\n- Chlorine: M and M+2 peaks in approximately 3:1 ratio (\u00b3\u2075Cl:\u00b3\u2077Cl = 3:1).\n- Two Br atoms: M, M+2, M+4 in 1:2:1 ratio.\n- Sulfur: Small M+2 peak (~4% of M) from \u00b3\u2074S.\nNo significant M+2 \u2192 no Cl, Br, or S."),

    ("How do you combine IR, NMR, and MS data to identify an unknown compound?",
     "Systematic approach:\n1. MS: Determine molecular weight (M\u207a) and molecular formula. Apply nitrogen rule. Check isotope patterns for Cl/Br.\n2. Calculate DEGREES OF UNSATURATION from molecular formula.\n3. IR: Identify functional groups. Key peaks: broad OH (3200\u20133600), C=O (1700), N\u2013H (3300\u20133500), C\u2261N (2200), very broad COOH (2500\u20133300).\n4. \u00b9H NMR: Count types of H (number of signals). Integration \u2192 number of H per signal. Chemical shifts \u2192 identify functional groups. Splitting \u2192 connectivity (n+1 rule).\n5. \u00b9\u00b3C NMR (if available): Number of unique carbons. DEPT to identify CH\u2083, CH\u2082, CH, quaternary C.\n6. Propose a structure consistent with ALL data. Verify by checking that every spectral feature matches."),
]


# ─── DECK DEFINITIONS ───
DECKS = [
    {
        "slug": "orgo-functional-groups",
        "title": "Organic Chemistry: Functional Groups & Nomenclature",
        "category": "College",
        "description": "All major organic functional groups, IUPAC naming rules, common names, physical properties, and intermolecular forces.",
        "meta_desc": "Free organic chemistry flashcards covering functional groups, IUPAC nomenclature, common names, and physical properties. Study online or import into Stacked.",
        "keywords": "organic chemistry flashcards, functional groups, IUPAC nomenclature, orgo study cards, organic chemistry naming",
        "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
        "cards": FUNCTIONAL_GROUPS_CARDS,
    },
    {
        "slug": "orgo-reactions-mechanisms",
        "title": "Organic Chemistry: Reactions & Mechanisms",
        "category": "College",
        "description": "SN1/SN2/E1/E2 mechanisms, addition reactions, oxidation/reduction, Grignard, EAS, and key reagent cards.",
        "meta_desc": "Free organic chemistry flashcards covering reactions and mechanisms: SN1, SN2, E1, E2, Grignard, EAS, and more. Study online or import into Stacked.",
        "keywords": "organic chemistry reactions, orgo mechanisms, SN1 SN2 E1 E2, Grignard reaction, organic chemistry flashcards",
        "color": {"hex": "#FF375F", "r": 1.0, "g": 0.216, "b": 0.373},
        "cards": REACTIONS_CARDS,
    },
    {
        "slug": "orgo-stereochemistry-spectroscopy",
        "title": "Organic Chemistry: Stereochemistry & Spectroscopy",
        "category": "College",
        "description": "Chirality, R/S configuration, conformational analysis, IR spectroscopy, NMR, and mass spectrometry.",
        "meta_desc": "Free organic chemistry flashcards covering stereochemistry, IR, NMR, and mass spectrometry. Study online or import into Stacked.",
        "keywords": "organic chemistry stereochemistry, NMR spectroscopy, IR spectroscopy, chirality flashcards, orgo spectroscopy",
        "color": {"hex": "#AF52DE", "r": 0.686, "g": 0.322, "b": 0.969},
        "cards": SPECTROSCOPY_CARDS,
    },
]

# ─── Load TEMPLATE from generate-decks.py ───
# Read the TEMPLATE variable from the existing generate-decks.py file
import re

gen_decks_path = os.path.join(SITE, "generate-decks.py")
with open(gen_decks_path, "r") as f:
    source = f.read()

# Extract the TEMPLATE string by executing just the assignment
# Find TEMPLATE = """...""" and extract it
match = re.search(r'TEMPLATE\s*=\s*"""(.*?)"""', source, re.DOTALL)
if not match:
    print("ERROR: Could not find TEMPLATE in generate-decks.py")
    sys.exit(1)

TEMPLATE = match.group(0).split('= ', 1)[1]
# Remove the triple-quote wrappers
TEMPLATE = TEMPLATE[3:-3]

# ─── Generate HTML pages ───
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
    print(f"Generated {deck['slug']}.html ({len(deck['cards'])} cards)")

# ─── Update catalog.json ───
catalog_path = os.path.join(SITE, "decks", "catalog.json")
with open(catalog_path, "r") as f:
    catalog = json.load(f)

# Remove any existing orgo entries to avoid duplicates
existing_slugs = {d["slug"] for d in DECKS}
catalog = [entry for entry in catalog if entry["slug"] not in existing_slugs]

# Add new entries
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
print(f"\nUpdated catalog.json with {len(DECKS)} new orgo decks")

print(f"\nDone! Generated {len(DECKS)} organic chemistry deck pages.")
