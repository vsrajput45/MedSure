import re
from typing import Dict, List, Tuple
from decimal import Decimal, ROUND_HALF_UP

class BillNormalizer:
    CATEGORY_KEYWORDS = {
        "IMPLANT": ["implant", "prosthesis", "femoral", "tibial", "stent", "mesh", "screw", "plate", "lens", "iol"],
        "SURGERY": ["ot charges", "operation theatre", "surgeon fee", "anesthesia", "anesthetist", "surgical team", "procedure fee"],
        "ROOM_RENT": ["room rent", "bed charges", "icu charges", "deluxe room", "general ward", "nursing care", "daily bed"],
        "PHARMACY": ["injection", "inj", "tab", "tablet", "syrup", "infusion", "ceftriaxone", "paracetamol", "antibiotic", "medication", "medicine"],
        "INVESTIGATION": ["x-ray", "mri", "ct scan", "blood test", "cbc", "pathology", "radiology", "biochemistry", "ecg", "ultrasound", "usg"],
        "CONSUMABLE": ["gloves", "syringe", "dressing", "gauze", "catheter", "ppe", "surgical kit", "drapes", "cannula", "cotton"],
        "NURSING": ["nursing fee", "nurse duty", "rMO charges", "resident doctor", "physiotherapy"]
    }

    def categorize_description(self, desc: str) -> str:
        d = desc.lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in d for kw in keywords):
                return category
        return "OTHER"

    def normalize_description(self, desc: str) -> str:
        # Remove extra punctuation, leading numbers, standardize capitalization
        clean = re.sub(r"^[0-9\s.:#-]+", "", desc).strip()
        clean = re.sub(r"\s+", " ", clean)
        return clean.title()

    def parse_line_items_from_text(self, raw_text: str) -> List[Dict]:
        """
        Parses OCR/PDF raw text into candidate line items.
        Handles invoice tabular formats with numbers, rates, quantities.
        """
        items = []
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        
        line_num = 1
        for line in lines:
            # Pattern matching: Description followed by numbers (Qty, Rate, Total)
            # Examples:
            # "1. Knee Implant High Flexion 1 85000.00 85000.00"
            # "OT Charges (Major Surgery) | 1 | 35000 | 35000"
            # "Inj Paracetamol 100ml IV   3   250.00   750.00"
            numbers = re.findall(r"[\d,]+(?:\.\d{1,2})?", line)
            
            # Filter numbers that look like quantities and monetary amounts
            valid_nums = []
            for n in numbers:
                clean_n = n.replace(",", "")
                try:
                    val = float(clean_n)
                    valid_nums.append((n, val))
                except ValueError:
                    continue
            
            # If we found at least 1 or 2 monetary-like numbers and non-numeric description
            desc_part = re.sub(r"[\d,.:|/\\₹Rs]+", " ", line).strip()
            if len(desc_part) > 3 and len(valid_nums) >= 1:
                # Discard date strings or invoice headers
                if any(hdr in desc_part.lower() for hdr in ["invoice", "date", "phone", "gst", "patient", "total", "subtotal", "tax"]):
                    continue

                if len(valid_nums) >= 3:
                    candidate_total = valid_nums[-1][1]
                    matched_pair = False
                    # Search for candidate (qty, unit_price) pair whose product matches candidate_total
                    for i in range(len(valid_nums) - 2):
                        for j in range(i + 1, len(valid_nums) - 1):
                            q_val = valid_nums[i][1]
                            p_val = valid_nums[j][1]
                            # Check if product matches total within 2% or 0.50 tolerance
                            if abs((q_val * p_val) - candidate_total) <= max(0.50, 0.02 * candidate_total):
                                qty = q_val
                                unit_price = p_val
                                total = candidate_total
                                matched_pair = True
                                break
                        if matched_pair:
                            break

                    if not matched_pair:
                        qty = valid_nums[-3][1] if valid_nums[-3][1] < 500 else 1.0
                        unit_price = valid_nums[-2][1]
                        total = candidate_total
                elif len(valid_nums) == 2:
                    qty = valid_nums[0][1] if valid_nums[0][1] < 100 else 1.0
                    unit_price = valid_nums[1][1]
                    total = unit_price * qty
                else:
                    qty = 1.0
                    unit_price = valid_nums[0][1]
                    total = unit_price

                category = self.categorize_description(desc_part)
                norm_desc = self.normalize_description(desc_part)

                items.append({
                    "line_number": line_num,
                    "raw_description": line,
                    "normalized_description": norm_desc,
                    "category": category,
                    "quantity": float(qty),
                    "unit_price": float(unit_price),
                    "line_total": float(total),
                    "extracted_line_total": float(total),
                    "ocr_confidence": 0.95,
                    "is_package_component": False,
                    "user_edited": False
                })
                line_num += 1

        return items

bill_normalizer = BillNormalizer()
