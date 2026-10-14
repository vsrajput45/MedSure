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
        "Orthopedics": [
            r"\b(knee|joint|bone|hip|spine|fracture|ligament|acl|arthritis|osteoarthritis|cartilage|ortho)\b",
            r"(घुटने|जोड़|हड्डी|कमर दर्द|गठिया|हड्डी टूटना)"
        ],
        "Cardiology": [
            r"\b(heart|cardiac|palpitation|chest pressure|angina|pulse|arrhythmia|ecg)\b",
            r"(दिल|धड़कन|दिल की धड़कन|कार्डियक)"
        ],
        "Gastroenterology": [
            r"\b(abdomen|stomach|gastric|gallbladder|appendix|appendicitis|cholecystitis|hernia|jaundice|liver|bowel|colon)\b",
            r"(पेट|पेट दर्द|अपेंडिक्स|पित्त की थैली|पीलिया|उल्टी|गैस)"
        ],
        "Ophthalmology": [
            r"\b(eye|vision|cataract|cornea|glaucoma|retina|blur|ophthal|lens)\b",
            r"(आँख|आंख|धुंधला|मोतियाबिंद|दृष्टि)"
        ],
        "Obstetrics & Gynecology": [
            r"\b(pregnancy|delivery|caesarean|c-section|labor|uterus|ovary|gynec)\b",
            r"(गर्भावस्था|प्रसव|डिलीवरी|सिजेरियन)"
        ],
        "Pulmonology": [
            r"\b(lung|cough|asthma|bronchitis|wheezing|respiratory|pneumonia)\b",
            r"(फेफड़े|खांसी|दमा|अस्थमा|कफ)"
        ],
        "General Surgery": [
            r"\b(surgery|wound|cyst|abscess|swelling|lump|incision)\b",
            r"(सर्जरी|ऑपरेशन|गांठ|सूजन)"
        ]
    }

    # Common Procedure Mapping
    PROCEDURE_PATTERNS = [
        {
            "code": "PROC-KNEE-TKR-01",
            "name": "Total Knee Replacement (Unilateral)",
            "specialty": "Orthopedics",
            "keywords": [
                "knee replacement", "knee osteoarthritis", "severe knee pain", "tkr", "knee surgery",
                "घुटने का प्रत्यारोपण", "घुटने का दर्द", "घुटने में दर्द", "घुटने में बहुत तेज दर्द", "घुटने"
            ]
        },
        {
            "code": "PROC-GI-APP-01",
            "name": "Laparoscopic Appendectomy",
            "specialty": "Gastroenterology",
            "keywords": ["appendicitis", "appendix pain", "appendix", "lower right abdominal pain", "अपेंडिक्स", "पेट के निचले हिस्से में दर्द"]
        },
        {
            "code": "PROC-GI-CHO-01",
            "name": "Laparoscopic Cholecystectomy (Gallbladder Removal)",
            "specialty": "Gastroenterology",
            "keywords": ["gallbladder stone", "gallstone", "cholecystectomy", "cholelithiasis", "पित्त की पथरी", "पित्ताशय"]
        },
        {
            "code": "PROC-OPH-CAT-01",
            "name": "Cataract Surgery with Foldable IOL (Phacoemulsification)",
            "specialty": "Ophthalmology",
            "keywords": ["cataract", "cloudy lens", "phaco", "eye lens", "मोतियाबिंद", "आंख का लेंस"]
        },
        {
            "code": "PROC-OBG-CS-01",
            "name": "Caesarean Section Delivery (C-Section)",
            "specialty": "Obstetrics & Gynecology",
            "keywords": ["c-section", "caesarean", "cesarean", "planned delivery", "सिजेरियन डिलीवरी"]
        },
        {
            "code": "PROC-CARD-ANGIO-01",
            "name": "Coronary Angiography",
            "specialty": "Cardiology",
            "keywords": ["angiography", "coronary angiogram", "heart block check", "एंजियोग्राफी"]
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

        # 4. Procedure Mapping
        matched_proc = None
        for proc in self.PROCEDURE_PATTERNS:
            for kw in proc["keywords"]:
                if kw.lower() in clean_text:
                    matched_proc = proc
                    break
            if matched_proc:
                break
        
        if matched_proc and identified_specialty == "General Medicine":
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
