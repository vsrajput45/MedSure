import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import fitz  # PyMuPDF
from PIL import Image

class OCRService:
    def calculate_file_hash(self, file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    def extract_text_from_pdf(self, file_path: Path) -> Tuple[str, bool]:
        """
        Extract native text from PDF using PyMuPDF safely.
        Returns (text, is_native_text)
        """
        full_text = []
        is_native = False
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                if text.strip():
                    is_native = True
                    full_text.append(text)
            doc.close()
        except Exception:
            return "", False
        
        combined_text = "\n".join(full_text)
        return combined_text, is_native

    def extract_text_from_image(self, file_path: Path) -> str:
        """
        Extract text from image using pytesseract if available, or fallback.
        """
        try:
            import pytesseract
            img = Image.open(file_path)
            # Basic preprocessing
            img_gray = img.convert('L')
            text = pytesseract.image_to_string(img_gray)
            return text
        except Exception:
            return ""

    def process_document(self, file_path: Path, mime_type: str) -> Dict:
        """
        Processes an uploaded PDF or image file and extracts text.
        """
        extracted_text = ""
        is_native = False

        if "pdf" in mime_type.lower() or file_path.suffix.lower() == ".pdf":
            extracted_text, is_native = self.extract_text_from_pdf(file_path)
            # If native extraction yielded very little text, attempt OCR on rendered pages
            if not extracted_text.strip():
                try:
                    import pytesseract
                    doc = fitz.open(file_path)
                    ocr_pages = []
                    for page_num in range(min(len(doc), 5)):
                        page = doc[page_num]
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        page_text = pytesseract.image_to_string(img)
                        ocr_pages.append(page_text)
                    doc.close()
                    extracted_text = "\n".join(ocr_pages)
                except Exception:
                    pass
        else:
            extracted_text = self.extract_text_from_image(file_path)

        metadata = self._parse_metadata(extracted_text)
        
        return {
            "raw_text": extracted_text,
            "is_native_text": is_native,
            "metadata": metadata
        }

    def _parse_metadata(self, text: str) -> Dict:
        metadata = {
            "hospital_name": None,
            "invoice_number": None,
            "bill_date": None,
            "patient_identifier": None,
            "total_claimed": None
        }
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Hospital Name heuristics
        for line in lines[:8]:
            if any(term in line.lower() for term in ["hospital", "healthcare", "clinic", "medicare", "medical centre", "memorial"]):
                metadata["hospital_name"] = line
                break
        
        # Invoice / Bill Number heuristics
        inv_match = re.search(r"(?:invoice|bill|receipt|bill\s+no|inv\s+no)[\s.:#-]+([A-Z0-9\/-]+)", text, re.IGNORECASE)
        if inv_match:
            metadata["invoice_number"] = inv_match.group(1).strip()

        # Date heuristics (DD/MM/YYYY or YYYY-MM-DD or DD-Mon-YYYY)
        date_match = re.search(r"(\b\d{1,2}[-\/.]\d{1,2}[-\/.]\d{2,4}\b|\b\d{4}[-\/.]\d{1,2}[-\/.]\d{1,2}\b)", text)
        if date_match:
            try:
                date_str = date_match.group(1).replace(".", "/").replace("-", "/")
                parts = date_str.split("/")
                if len(parts[0]) == 4:
                    metadata["bill_date"] = datetime(int(parts[0]), int(parts[1]), int(parts[2]), tzinfo=timezone.utc)
                else:
                    year = int(parts[2])
                    if year < 100:
                        year += 2000
                    p0 = int(parts[0])
                    p1 = int(parts[1])
                    # Handle both DD/MM and MM/DD
                    if p0 > 12:
                        day, month = p0, p1
                    elif p1 > 12:
                        day, month = p1, p0
                    else:
                        day, month = p0, p1
                    metadata["bill_date"] = datetime(year, month, day, tzinfo=timezone.utc)
            except Exception:
                metadata["bill_date"] = datetime.now(timezone.utc)

        # Total Amount heuristics
        total_match = re.search(r"(?:grand\s+total|total\s+amount|net\s+payable|total\s+bill)[\s.:₹RsINR]*([\d,]+(?:\.\d{1,2})?)", text, re.IGNORECASE)
        if total_match:
            try:
                val = float(total_match.group(1).replace(",", ""))
                metadata["total_claimed"] = val
            except Exception:
                pass

        return metadata

ocr_service = OCRService()
