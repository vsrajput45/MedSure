import re
from typing import Dict, List, Tuple

class TriageService:
    # Emergency red flags (English and Hindi transliterated / Devanagari)
    EMERGENCY_KEYWORDS = [
        "chest pain", "pressure in chest", "shortness of breath", "difficulty breathing",
        "sudden weakness", "facial drooping", "slurred speech", "paralysis",
        "uncontrolled bleeding", "loss of consciousness", "fainting", "severe head injury",
        "coughing up blood", "vomiting blood", "bluish lips", "seizure",
        # Hindi
        "सीने में दर्द", "सांस लेने में तकलीफ", "सांस फूलना", "बेहोश", "बेहोशी",
        "खून की उल्टी", "अचानक लकवा", "चेहरे का टेढ़ा होना", "अत्यधिक खून बहना"
    ]

    URGENT_KEYWORDS = [
        "high fever", "severe abdominal pain", "deep cut", "fracture", "broken bone",
        "inability to walk", "severe dehydration", "persistent vomiting", "acute pain",
        # Hindi
        "तेज बुखार", "असहनीय पेट दर्द", "हड्डी टूटना", "गहरा घाव", "लगातार उल्टी"
    ]

    # Clinical Specialty Knowledge Base
    SPECIALTY_PATTERNS = {
        "General Medicine": [
            r"\b(fever|cough|cold|headache|stomach ache|stomach pain|gas|acidity|indigestion|loose motion|diarrhea|vomiting|nausea|badan dard|kamzori|weakness|fatigue|sore throat|sneezing|flu|mild|malaise|runny nose|chills)\b",
            r"(बुखार|खांसी|सर्दी|जुकाम|सिरदर्द|सिर दर्द|पेट दर्द|उल्टी|दस्त|कमजोरी|थकान|बदन दर्द|गैस|एसिडिटी|गले में खराश|गला खराब|छींक|हल्का बुखार)"
        ],
        "Orthopedics": [
            r"\b(knee|joint|bone|hip|spine|fracture|ligament|acl|arthritis|osteoarthritis|cartilage|ortho|shoulder|dislocation|back pain)\b",
            r"(घुटने|जोड़|हड्डी|कमर दर्द|गठिया|हड्डी टूटना|फ्रैक्चर|कूल्हा|प्लास्टर)"
        ],
        "Cardiology": [
            r"\b(heart|cardiac|palpitation|chest pressure|angina|pulse|arrhythmia|ecg|bypass|cabg|stent|angioplasty|heart attack)\b",
            r"(दिल|धड़कन|दिल की धड़कन|कार्डियक|बायपास|हार्ट अटैक|स्टेंट)"
        ],
        "Gastroenterology": [
            r"\b(gallbladder|appendix|appendicitis|cholecystitis|hernia|jaundice|liver|bowel|colon|piles|fissure|fistula|ulcer|endoscopy|colonoscopy|severe abdominal pain)\b",
            r"(अपेंडिक्स|पित्त की थैली|पीलिया|बवासीर|पाइल्स|हर्निया|गंभीर पेट दर्द|एंडोस्कोपी)"
        ],
        "Urology & Nephrology": [
            r"\b(kidney|renal|stone|lithotripsy|urinary|urine|prostate|turp|dialysis|creatinine|bladder)\b",
            r"(गुर्दा|किडनी|पथरी|पेशाब|प्रोस्टेट|डायलिसिस)"
        ],
        "Ophthalmology": [
            r"\b(eye|vision|cataract|cornea|glaucoma|retina|blur|ophthal|lens|lasik|spectacles)\b",
            r"(आँख|आंख|धुंधला|मोतियाबिंद|दृष्टि|चश्मा)"
        ],
        "Obstetrics & Gynecology": [
            r"\b(pregnancy|delivery|caesarean|c-section|labor|uterus|ovary|gynec|hysterectomy|period|pcod|pcos)\b",
            r"(गर्भावस्था|प्रसव|डिलीवरी|सिजेरियन|बच्चेदानी|मासिक धर्म)"
        ],
        "Pulmonology": [
            r"\b(lung|asthma|bronchitis|wheezing|respiratory|pneumonia|tuberculosis|tb|breathless|copd|inhaler)\b",
            r"(फेफड़े|दमा|अस्थमा|निमोनिया|टीबी|सांस फूलना)"
        ],
        "Neurology": [
            r"\b(brain|neuro|nerve|severe migraine|stroke|paralysis|seizure|epilepsy|vertigo|convulsion)\b",
            r"(दिमाग|लकवा|दौरा|चक्कर|मस्तिष्क|पक्षाघात)"
        ],
        "ENT": [
            r"\b(ear|nose|tonsil|sinus|sinusitis|hearing|dns|septoplasty|ear pain|ear discharge)\b",
            r"(कान|नाक|टॉन्सिल|साइनस|कान बहना|कान में दर्द)"
        ],
        "Internal Medicine & Infectious Diseases": [
            r"\b(dengue|malaria|typhoid|platelet|chikungunya|covid|sepsis|high fever with chills)\b",
            r"(डेंगू|मलेरिया|टाइफाइड|प्लेटलेट|संक्रमण)"
        ],
        "General Surgery": [
            r"\b(surgery|wound|cyst|abscess|swelling|lump|incision|operation)\b",
            r"(सर्जरी|ऑपरेशन|गांठ|सूजन|घाव)"
        ]
    }

    # Common Procedure Mapping
    PROCEDURE_PATTERNS = [
        # 1. Total Knee Replacement
        {
            "code": "PROC-KNEE-TKR-01",
            "name": "Total Knee Replacement (Unilateral)",
            "specialty": "Orthopedics",
            "keywords": [
                "knee replacement", "knee osteoarthritis", "severe knee pain", "tkr", "knee surgery",
                "ghutne ka operation", "ghutne me dard", "ghutne ka dard",
                "घुटने का प्रत्यारोपण", "घुटने का दर्द", "घुटने में दर्द", "घुटने में बहुत तेज दर्द", "घुटने का ऑपरेशन"
            ]
        },
        # 2. Total Hip Replacement
        {
            "code": "PROC-ORTHO-THR-01",
            "name": "Total Hip Replacement (THR)",
            "specialty": "Orthopedics",
            "keywords": [
                "hip replacement", "hip arthroplasty", "thr", "hip fracture surgery", "hip pain severe",
                "koolhe ka operation", "hip operation",
                "कूल्हे का प्रत्यारोपण", "हिप रिप्लेसमेंट", "कूल्हे की हड्डी"
            ]
        },
        # 3. Bone Fracture Treatment & Plaster/Fixation
        {
            "code": "PROC-ORTHO-FRAC-01",
            "name": "Bone Fracture Reduction & Internal Fixation",
            "specialty": "Orthopedics",
            "keywords": [
                "fracture", "broken bone", "bone fracture", "hairline fracture", "plaster", "cast", "bone surgery",
                "haddi toot", "haddi crack",
                "हड्डी टूटना", "फ्रैक्चर", "हड्डी टूट गई", "प्लास्टर", "हड्डी क्रैक"
            ]
        },
        # 4. ACL / Ligament Reconstruction
        {
            "code": "PROC-ORTHO-ACL-01",
            "name": "Arthroscopic ACL / Knee Ligament Reconstruction",
            "specialty": "Orthopedics",
            "keywords": [
                "acl", "ligament", "arthroscopy", "knee ligament tear", "meniscus tear",
                "लिगामेंट", "आर्थोस्कोपी", "लिगामेंट टियर"
            ]
        },
        # 5. Spine Surgery / Slip Disc Discectomy
        {
            "code": "PROC-ORTHO-SPINE-01",
            "name": "Lumbar Discectomy / Spine Decompression Surgery",
            "specialty": "Orthopedics",
            "keywords": [
                "slip disc", "spine surgery", "sciatica", "disc bulge", "lumbar spine", "back surgery",
                "स्लिप डिस्क", "रीढ़ की हड्डी का ऑपरेशन", "साइटिका"
            ]
        },
        # 6. Laparoscopic Appendectomy
        {
            "code": "PROC-GI-APP-01",
            "name": "Laparoscopic Appendectomy",
            "specialty": "Gastroenterology",
            "keywords": [
                "appendicitis", "appendix pain", "appendix", "lower right abdominal pain", "appendix ka dard", "appendix operation",
                "अपेंडिक्स", "पेट के निचले हिस्से में दर्द", "अपेंडिक्स का ऑपरेशन"
            ]
        },
        # 7. Laparoscopic Cholecystectomy
        {
            "code": "PROC-GI-CHO-01",
            "name": "Laparoscopic Cholecystectomy (Gallbladder Removal)",
            "specialty": "Gastroenterology",
            "keywords": [
                "gallbladder stone", "gallstone", "cholecystectomy", "cholelithiasis", "gallbladder pain",
                "pitt ki thaili me pathri", "pitt ki thaili", "gallbladder pathri",
                "पित्त की पथरी", "पित्ताशय", "पित्त की थैली में पथरी"
            ]
        },
        # 8. Hernia Repair Surgery
        {
            "code": "PROC-SURG-HERNIA-01",
            "name": "Inguinal / Umbilical Hernia Repair Surgery",
            "specialty": "General Surgery",
            "keywords": [
                "hernia", "inguinal hernia", "umbilical hernia", "herniotomy", "hernioplasty",
                "हर्निया", "हर्निया का ऑपरेशन"
            ]
        },
        # 9. Piles / Hemorrhoids Surgery
        {
            "code": "PROC-SURG-PILES-01",
            "name": "Laser Hemorrhoidectomy (Piles / Fissure Surgery)",
            "specialty": "General Surgery",
            "keywords": [
                "piles", "hemorrhoids", "fissure", "fistula", "bleeding during stool",
                "बवासीर", "पाइल्स", "भगंदर", "फिशर"
            ]
        },
        # 10. Upper GI Endoscopy
        {
            "code": "PROC-GI-ENDO-01",
            "name": "Diagnostic Upper GI Endoscopy & Colonoscopy",
            "specialty": "Gastroenterology",
            "keywords": [
                "endoscopy", "colonoscopy", "gastroscopy", "stomach endoscopy",
                "एंडोस्कोपी", "कोलोनोस्कोपी"
            ]
        },
        # 11. Kidney Stone Removal (Lithotripsy/PCNL)
        {
            "code": "PROC-URO-STONE-01",
            "name": "Kidney Stone Laser Removal (PCNL / URSL / Lithotripsy)",
            "specialty": "Urology & Nephrology",
            "keywords": [
                "kidney stone", "renal stone", "renal calculus", "lithotripsy", "pcnl", "ursl", "ureteric stone",
                "gurde ki pathri", "gurde me pathri", "kidney pathri", "pathri",
                "गुर्दे की पथरी", "किडनी स्टोन", "पथरी का ऑपरेशन", "किडनी में पथरी", "पथरी"
            ]
        },
        # 12. TURP Prostate Surgery
        {
            "code": "PROC-URO-TURP-01",
            "name": "Transurethral Resection of Prostate (TURP)",
            "specialty": "Urology & Nephrology",
            "keywords": [
                "prostate surgery", "turp", "enlarged prostate", "bph", "difficulty passing urine",
                "प्रोस्टेट", "पौरुष ग्रंथि", "पेशाब में रुकावट"
            ]
        },
        # 13. Hemodialysis Package
        {
            "code": "PROC-NEPH-DIAL-01",
            "name": "Hemodialysis Session & Care Package",
            "specialty": "Urology & Nephrology",
            "keywords": [
                "dialysis", "hemodialysis", "kidney failure", "renal failure", "high creatinine",
                "डायलिसिस", "किडनी फेलियर", "गुर्दा खराब"
            ]
        },
        # 14. Cataract Surgery with Foldable IOL
        {
            "code": "PROC-OPH-CAT-01",
            "name": "Cataract Surgery with Foldable IOL (Phacoemulsification)",
            "specialty": "Ophthalmology",
            "keywords": [
                "cataract", "cloudy lens", "phaco", "eye lens", "cataract surgery",
                "मोतियाबिंद", "आंख का लेंस", "मोतियाबिंद का ऑपरेशन"
            ]
        },
        # 15. LASIK Eye Surgery
        {
            "code": "PROC-OPH-LASIK-01",
            "name": "Customized Contoura LASIK Laser Eye Surgery",
            "specialty": "Ophthalmology",
            "keywords": [
                "lasik", "laser eye surgery", "specs removal", "laser vision",
                "लेसिक", "चश्मा हटाने का ऑपरेशन", "आंखों का लेजर"
            ]
        },
        # 16. Caesarean Section Delivery
        {
            "code": "PROC-OBG-CS-01",
            "name": "Caesarean Section Delivery (C-Section)",
            "specialty": "Obstetrics & Gynecology",
            "keywords": [
                "c-section", "caesarean", "cesarean", "planned c-section", "surgical delivery",
                "सिजेरियन", "सिजेरियन डिलीवरी", "ऑपरेशन से डिलीवरी"
            ]
        },
        # 17. Normal Vaginal Delivery
        {
            "code": "PROC-OBG-NVD-01",
            "name": "Normal Vaginal Delivery Care Package",
            "specialty": "Obstetrics & Gynecology",
            "keywords": [
                "normal delivery", "natural childbirth", "vaginal delivery", "maternity delivery",
                "सामान्य प्रसव", "नॉर्मल डिलीवरी", "डिलीवरी"
            ]
        },
        # 18. Hysterectomy (Uterus Removal)
        {
            "code": "PROC-OBG-HYST-01",
            "name": "Total Laparoscopic / Abdominal Hysterectomy (Uterus Removal)",
            "specialty": "Obstetrics & Gynecology",
            "keywords": [
                "hysterectomy", "uterus removal", "fibroid uterus", "uterine prolapse",
                "बच्चेदानी का ऑपरेशन", "हिस्टेरेक्टॉमी", "बच्चेदानी निकालना"
            ]
        },
        # 19. Coronary Angiography
        {
            "code": "PROC-CARD-ANGIO-01",
            "name": "Coronary Angiography",
            "specialty": "Cardiology",
            "keywords": [
                "angiography", "coronary angiogram", "heart block check", "cag",
                "एंजियोग्राफी", "दिल की नसों की जांच"
            ]
        },
        # 20. Coronary Angioplasty with Stent (PTCA)
        {
            "code": "PROC-CARD-PTCA-01",
            "name": "Coronary Angioplasty with Drug-Eluting Stent (PTCA)",
            "specialty": "Cardiology",
            "keywords": [
                "angioplasty", "stent", "drug eluting stent", "ptca", "heart blockage treatment", "coronary stent",
                "एंजियोप्लास्टी", "स्टेंट", "हार्ट स्टेंट", "छल्ला डालना", "नसों में ब्लॉकेज"
            ]
        },
        # 21. Coronary Artery Bypass Graft (CABG)
        {
            "code": "PROC-CARD-CABG-01",
            "name": "Coronary Artery Bypass Graft (CABG / Open Heart Bypass)",
            "specialty": "Cardiology",
            "keywords": [
                "bypass surgery", "cabg", "coronary bypass", "open heart surgery", "triple vessel disease",
                "बायपास सर्जरी", "ओपन हार्ट सर्जरी", "बायपास"
            ]
        },
        # 22. Pacemaker Implantation
        {
            "code": "PROC-CARD-PACE-01",
            "name": "Permanent Cardiac Pacemaker Implantation (Dual Chamber)",
            "specialty": "Cardiology",
            "keywords": [
                "pacemaker", "cardiac pacemaker", "slow heart rate", "heart block pacemaker",
                "पेसमेकर", "पेसमेकर प्रत्यारोपण"
            ]
        },
        # 23. Dengue Inpatient Management
        {
            "code": "PROC-MED-DENGUE-01",
            "name": "Inpatient Dengue Management & Thrombocytopenia Care",
            "specialty": "Internal Medicine & Infectious Diseases",
            "keywords": [
                "dengue", "dengue fever", "low platelets", "platelet count drop", "dengue hemorrhagic",
                "डेंगू", "डेंगू बुखार", "प्लेटलेट्स कम", "प्लेटलेट"
            ]
        },
        # 24. Typhoid / Enteric Fever Management
        {
            "code": "PROC-MED-TYPHOID-01",
            "name": "Inpatient Enteric Fever (Typhoid) Treatment",
            "specialty": "Internal Medicine & Infectious Diseases",
            "keywords": [
                "typhoid", "enteric fever", "widal positive", "typhoid fever",
                "टाइफाइड", "मियादी बुखार", "मोतीझरा"
            ]
        },
        # 25. Malaria Inpatient Care
        {
            "code": "PROC-MED-MALARIA-01",
            "name": "Inpatient Acute Malaria Treatment & Care",
            "specialty": "Internal Medicine & Infectious Diseases",
            "keywords": [
                "malaria", "falciparum", "vivax", "shivering fever",
                "मलेरिया", "मलेरिया बुखार", "कंपकंपी के साथ बुखार"
            ]
        },
        # 26. Persistent / Extended Febrile Infection Diagnostic Profile
        {
            "code": "PROC-MED-FEVER-01",
            "name": "Acute Viral Fever & Infection Diagnostic Workup",
            "specialty": "Internal Medicine & Infectious Diseases",
            "keywords": [
                "persistent fever", "chronic fever", "fever panel", "unexplained fever", "fever workup",
                "high fever persistent", "लगातार बुखार", "कई दिनों से बुखार", "बुखार की जांच", "फीवर प्रोफाइल"
            ]
        },
        # 27. Severe Pneumonia Inpatient Care
        {
            "code": "PROC-MED-PNEUMO-01",
            "name": "Inpatient Severe Pneumonia & Bronchitis Care",
            "specialty": "Pulmonology",
            "keywords": [
                "pneumonia", "chest infection", "lung infection", "severe bronchitis", "phlegm cough",
                "निमोनिया", "फेफड़ों में संक्रमण", "कफ और सांस फूलना"
            ]
        },
        # 28. Tonsillectomy
        {
            "code": "PROC-ENT-TONS-01",
            "name": "Tonsillectomy with Adenoidectomy",
            "specialty": "ENT",
            "keywords": [
                "tonsils", "tonsillectomy", "tonsillitis", "throat infection recurring",
                "टॉन्सिल", "टॉन्सिल का ऑपरेशन", "गले में टॉन्सिल"
            ]
        },
        # 29. Septoplasty (DNS Repair)
        {
            "code": "PROC-ENT-SEPTO-01",
            "name": "Septoplasty (Deviated Nasal Septum Repair)",
            "specialty": "ENT",
            "keywords": [
                "septoplasty", "deviated septum", "dns", "crooked nose bone", "nasal blockage",
                "नाक की हड्डी", "नाक की हड्डी का ऑपरेशन", "सेप्टोप्लास्टी"
            ]
        },
        # 30. Acute Stroke ICU Stabilization
        {
            "code": "PROC-NEURO-STROKE-01",
            "name": "Acute Ischemic Stroke / Paralysis ICU Stabilization",
            "specialty": "Neurology",
            "keywords": [
                "stroke", "brain hemorrhage", "paralysis", "hemiplegia", "brain attack",
                "लकवा", "स्ट्रोक", "ब्रेन स्ट्रोक", "पक्षाघात", "फालिज"
            ]
        },
        # 31. MRI Scan
        {
            "code": "PROC-RAD-MRI-01",
            "name": "Magnetic Resonance Imaging (MRI Scan - Brain/Spine/Joint)",
            "specialty": "Radiology",
            "keywords": [
                "mri", "mri scan", "mri brain", "mri spine", "mri knee",
                "एमआरआई", "एमआरआई स्कैन"
            ]
        },
        # 32. CT Scan
        {
            "code": "PROC-RAD-CT-01",
            "name": "Computed Tomography (CT Scan - Head/Chest/Abdomen)",
            "specialty": "Radiology",
            "keywords": [
                "ct scan", "ncct head", "cect abdomen", "hrct chest",
                "सीटी स्कैन", "सीटी स्कैन सिर"
            ]
        },
        # 33. Whole Abdomen Ultrasound (USG)
        {
            "code": "PROC-RAD-USG-01",
            "name": "Whole Abdomen & Pelvis Ultrasound (USG)",
            "specialty": "Radiology",
            "keywords": [
                "ultrasound", "sonography", "usg abdomen", "usg",
                "अल्ट्रासाउंड", "सोनोग्राफी", "पेट का अल्ट्रासाउंड"
            ]
        },
        # 34. Routine Viral Fever & Flu OPD Care
        {
            "code": "PROC-OPD-FEVER-01",
            "name": "Routine Viral Fever & Flu Outpatient Care (OPD)",
            "specialty": "General Medicine",
            "keywords": [
                "viral fever", "mild fever", "fever", "bukhar", "halka bukhar", "temperature", "bodyache fever", "flu",
                "बुखार", "वायरल बुखार", "हल्का बुखार", "बुखार आ रहा है", "शरीर गरम है"
            ]
        },
        # 35. Common Cold, Cough & Sore Throat OPD Care
        {
            "code": "PROC-OPD-COUGH-01",
            "name": "Common Cold, Cough & Sore Throat Outpatient Care (OPD)",
            "specialty": "General Medicine",
            "keywords": [
                "cough and cold", "dry cough", "wet cough", "cough", "cold", "khasi", "sardi", "zukam", "zukaam",
                "sore throat", "runny nose", "sneezing", "throat irritation", "throat infection",
                "खांसी", "जुकाम", "सर्दी", "कफ", "सूखी खांसी", "गले में दर्द", "गले में खराश", "छींक"
            ]
        },
        # 36. Tension Headache & Mild Migraine OPD Care
        {
            "code": "PROC-OPD-HEADACHE-01",
            "name": "Tension Headache & Mild Migraine Outpatient Consultation",
            "specialty": "General Medicine",
            "keywords": [
                "mild headache", "tension headache", "headache", "sir dard", "sar dard", "sir me dard", "sar me dard", "head pain",
                "सिरदर्द", "सिर दर्द", "सर दर्द", "सिर में दर्द"
            ]
        },
        # 37. Acute Gastric Discomfort, Acidity & Diarrhea OPD Care
        {
            "code": "PROC-OPD-GASTRO-01",
            "name": "Acute Gastric Discomfort, Acidity & Mild Diarrhea Primary Care (OPD)",
            "specialty": "General Medicine",
            "keywords": [
                "mild stomach pain", "stomach pain", "stomach ache", "pet dard", "pet me dard", "acidity", "gas",
                "indigestion", "heartburn", "loose motion", "diarrhea", "vomiting", "nausea", "dast", "ulti", "pet kharab",
                "पेट दर्द", "पेट में दर्द", "गैस", "एसिडिटी", "उल्टी", "दस्त", "अपच", "जी मिचलाना"
            ]
        },
        # 38. General Routine Physician OPD Consultation
        {
            "code": "PROC-OPD-GEN-01",
            "name": "General Physician OPD Consultation & Routine Primary Care",
            "specialty": "General Medicine",
            "keywords": [
                "body ache", "badan dard", "kamzori", "weakness", "fatigue", "thakan", "tiredness", "malaise",
                "doctor consultation", "general checkup", "opd consultation", "doctor consult",
                "बदन दर्द", "कमजोरी", "थकान", "डॉक्टर परामर्श", "सामान्य जांच"
            ]
        },
        # 39. Complete Blood Count (CBC / Hemogram)
        {
            "code": "PROC-DIAG-CBC-01",
            "name": "Complete Blood Count (CBC / Hemogram)",
            "specialty": "Pathology",
            "keywords": [
                "cbc", "complete blood count", "hemogram", "blood test cbc",
                "सीबीसी", "खून की जांच सीबीसी"
            ]
        }
    ]

    def assess(self, query: str, preferred_language: str = "en") -> Dict:
        clean_text = query.strip().lower()
        
        # 1. Check Emergency Warning Signs
        emergency_signs = []
        for kw in self.EMERGENCY_KEYWORDS:
            if kw.lower() in clean_text:
                emergency_signs.append(kw)
        
        if emergency_signs:
            return {
                "urgency_level": "EMERGENCY",
                "is_emergency": True,
                "emergency_warning_signs": emergency_signs,
                "identified_specialty": "Emergency Medicine & Trauma",
                "recommended_action_en": (
                    "CRITICAL: Potential emergency warning sign detected. "
                    "Do NOT delay care for price estimation. Please seek immediate attention "
                    "at the nearest hospital emergency room or dial emergency services (112 / 102)."
                ),
                "recommended_action_hi": (
                    "अत्यंत महत्वपूर्ण: आपातकालीन लक्षण की पहचान हुई है। "
                    "लागत अनुमान के लिए समय न गवाएं। कृपया निकटतम अस्पताल के आपातकालीन विभाग में तुरंत जाएं "
                    "या 112 / 102 पर संपर्क करें।"
                ),
                "candidate_procedure_code": None,
                "candidate_procedure_name": None,
                "confidence_score": 0.95,
                "safety_disclaimer": (
                    "MEDSURE is an informational guidance tool and never provides clinical diagnoses or medical advice. "
                    "Emergency symptoms require immediate physical clinical evaluation."
                )
            }
        
        # 2. Check Urgent indicators
        is_urgent = any(kw.lower() in clean_text for kw in self.URGENT_KEYWORDS)
        urgency_level = "URGENT" if is_urgent else "ROUTINE"

        # 3. Identify Medical Specialty
        identified_specialty = "General Medicine"
        specialty_scores = {}
        for specialty, patterns in self.SPECIALTY_PATTERNS.items():
            score = 0
            for pat in patterns:
                matches = re.findall(pat, clean_text, re.IGNORECASE)
                score += len(matches)
            if score > 0:
                specialty_scores[specialty] = score
        
        if specialty_scores:
            identified_specialty = max(specialty_scores, key=specialty_scores.get)

        # 4. Procedure Mapping - Prioritize the most specific (longest keyword) match
        matched_candidates = []
        for proc in self.PROCEDURE_PATTERNS:
            for kw in proc["keywords"]:
                if kw.lower() in clean_text:
                    matched_candidates.append((len(kw), proc))
                    break
        
        matched_proc = None
        if matched_candidates:
            matched_candidates.sort(key=lambda x: x[0], reverse=True)
            matched_proc = matched_candidates[0][1]
        
        if matched_proc:
            identified_specialty = matched_proc["specialty"]

        # Guidance text generation
        action_en = f"Recommended consultation: {identified_specialty}. "
        action_hi = f"अनुशंसित विशेषज्ञ परामर्श: {identified_specialty}। "
        
        if matched_proc:
            action_en += f"Based on your description, this may involve procedural care such as '{matched_proc['name']}'. We have retrieved applicable fair price benchmarks below."
            action_hi += f"आपके विवरण के अनुसार, इसमें '{matched_proc['name']}' जैसी प्रक्रिया शामिल हो सकती है। हमने नीचे निष्पक्ष मूल्य बेंचमार्क जोड़े हैं।"
        else:
            action_en += "Please consult an accredited specialist for comprehensive physical evaluation and diagnostic tests before scheduling elective procedures."
            action_hi += "कृपया वैकल्पिक प्रक्रिया तय करने से पहले विस्तृत जांच के लिए किसी मान्यता प्राप्त विशेषज्ञ से परामर्श करें।"

        return {
            "urgency_level": urgency_level,
            "is_emergency": False,
            "emergency_warning_signs": [],
            "identified_specialty": identified_specialty,
            "recommended_action_en": action_en,
            "recommended_action_hi": action_hi,
            "candidate_procedure_code": matched_proc["code"] if matched_proc else None,
            "candidate_procedure_name": matched_proc["name"] if matched_proc else None,
            "confidence_score": 0.88 if matched_proc else 0.75,
            "safety_disclaimer": (
                "MEDSURE guidance is strictly educational and non-diagnostic. "
                "Always consult qualified healthcare professionals before undergoing treatments."
            )
        }

triage_service = TriageService()
