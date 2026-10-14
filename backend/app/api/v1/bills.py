import os
import uuid
from typing import List, Optional
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional
from app.core.config import settings
from app.models.all_models import Bill, BillLineItem, User
from app.schemas.bill import BillResponse, BillExtractionReviewResponse, LineItemsUpdate, BillLineItemSchema
from app.services.ocr.ocr_service import ocr_service
from app.services.normalization.bill_normalizer import bill_normalizer

router = APIRouter(prefix="/bills", tags=["Medical Bills"])

@router.post("/upload", response_model=BillExtractionReviewResponse, status_code=status.HTTP_201_CREATED)
async def upload_bill(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # 1. Validation: extension and content type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    file_bytes = await file.read()
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    file_hash = ocr_service.calculate_file_hash(file_bytes)
    user_id = current_user.id if current_user else None

    # Check duplicate file upload ONLY for the same user or public demo samples to prevent cross-user data leakage
    existing_bill = db.query(Bill).filter(Bill.file_hash == file_hash).first()
    if existing_bill and (existing_bill.is_demo_sample or (user_id and existing_bill.user_id == user_id)):
        # Return existing bill extraction
        line_items = db.query(BillLineItem).filter(BillLineItem.bill_id == existing_bill.id).order_by(BillLineItem.line_number).all()
        return BillExtractionReviewResponse(
            bill_id=existing_bill.id,
            hospital_name=existing_bill.hospital_name,
            invoice_number=existing_bill.invoice_number,
            bill_date=existing_bill.bill_date,
            patient_identifier=existing_bill.patient_identifier,
            total_claimed=existing_bill.total_amount_claimed,
            total_calculated=existing_bill.total_amount_calculated,
            line_items_count=len(line_items),
            line_items=[BillLineItemSchema.model_validate(it) for it in line_items],
            raw_ocr_preview=existing_bill.original_ocr_text[:500] if existing_bill.original_ocr_text else None
        )

    # Save file privately with secure UUID filename
    internal_filename = f"{uuid.uuid4()}{file_ext}"
    saved_path = settings.UPLOAD_DIR / internal_filename
    with open(saved_path, "wb") as f:
        f.write(file_bytes)

    # 2. Document Extraction & OCR
    extraction = ocr_service.process_document(saved_path, file.content_type or "application/octet-stream")
    raw_text = extraction["raw_text"]
    meta = extraction["metadata"]

    # 3. Normalization Pipeline
    parsed_items = bill_normalizer.parse_line_items_from_text(raw_text)

    # Calculate totals
    calculated_total = sum(item["line_total"] for item in parsed_items)
    claimed_total = meta["total_claimed"] or calculated_total

    # Sanitize client-provided filename
    safe_filename = Path(file.filename).name

    # 4. Save Bill record in Database
    bill = Bill(
        user_id=user_id,
        file_name=safe_filename,
        file_path=str(saved_path),
        file_hash=file_hash,
        file_size_bytes=len(file_bytes),
        mime_type=file.content_type or "application/octet-stream",
        hospital_name=meta["hospital_name"] or "Healthcare Provider",
        invoice_number=meta["invoice_number"] or f"INV-{uuid.uuid4().hex[:6].upper()}",
        bill_date=meta["bill_date"],
        extraction_status="EXTRACTED",
        original_ocr_text=raw_text,
        total_amount_claimed=claimed_total,
        total_amount_calculated=calculated_total,
        is_demo_sample=False
    )
    db.add(bill)
    db.flush()

    # Save Line items
    saved_line_items = []
    for item_data in parsed_items:
        item = BillLineItem(
            bill_id=bill.id,
            line_number=item_data["line_number"],
            raw_description=item_data["raw_description"],
            normalized_description=item_data["normalized_description"],
            category=item_data["category"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"],
            line_total=item_data["line_total"],
            extracted_line_total=item_data["extracted_line_total"],
            ocr_confidence=item_data["ocr_confidence"],
            is_package_component=item_data["is_package_component"]
        )
        db.add(item)
        saved_line_items.append(item)

    db.commit()
    db.refresh(bill)

    return BillExtractionReviewResponse(
        bill_id=bill.id,
        hospital_name=bill.hospital_name,
        invoice_number=bill.invoice_number,
        bill_date=bill.bill_date,
        patient_identifier=bill.patient_identifier,
        total_claimed=bill.total_amount_claimed,
        total_calculated=bill.total_amount_calculated,
        line_items_count=len(saved_line_items),
        line_items=[BillLineItemSchema.model_validate(it) for it in saved_line_items],
        raw_ocr_preview=raw_text[:500] if raw_text else None
    )

@router.get("", response_model=List[BillResponse])
def get_bills(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Bill)
    if current_user:
        query = query.filter((Bill.user_id == current_user.id) | (Bill.is_demo_sample == True))
    else:
        query = query.filter(Bill.is_demo_sample == True)
    
    bills = query.order_by(Bill.created_at.desc()).limit(20).all()
    return [BillResponse.model_validate(b) for b in bills]

@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(
    bill_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Ownership verification
    if not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this medical bill.")
            
    return BillResponse.model_validate(bill)

@router.get("/{bill_id}/extraction", response_model=BillExtractionReviewResponse)
def get_bill_extraction(
    bill_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Ownership verification
    if not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this extraction.")
    
    line_items = db.query(BillLineItem).filter(BillLineItem.bill_id == bill_id).order_by(BillLineItem.line_number).all()
    
    return BillExtractionReviewResponse(
        bill_id=bill.id,
        hospital_name=bill.hospital_name,
        invoice_number=bill.invoice_number,
        bill_date=bill.bill_date,
        patient_identifier=bill.patient_identifier,
        total_claimed=bill.total_amount_claimed,
        total_calculated=bill.total_amount_calculated,
        line_items_count=len(line_items),
        line_items=[BillLineItemSchema.model_validate(it) for it in line_items],
        raw_ocr_preview=bill.original_ocr_text[:500] if bill.original_ocr_text else None
    )

@router.patch("/{bill_id}/line-items", response_model=BillExtractionReviewResponse)
def update_bill_line_items(
    bill_id: str,
    update: LineItemsUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    # Disallow unauthorized modification
    if not bill.is_demo_sample and bill.user_id is not None:
        if not current_user or bill.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to modify this bill's line items.")

    # Clear existing and replace with user-corrected items
    db.query(BillLineItem).filter(BillLineItem.bill_id == bill_id).delete()
    
    updated_items = []
    total_calc = 0.0
    for idx, item in enumerate(update.items, 1):
        line_tot = item.quantity * item.unit_price
        total_calc += line_tot
        new_item = BillLineItem(
            bill_id=bill_id,
            line_number=idx,
            raw_description=item.raw_description,
            normalized_description=item.normalized_description,
            category=item.category,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.line_total if item.line_total > 0 else line_tot,
            extracted_line_total=item.extracted_line_total,
            user_edited=True,
            ocr_confidence=1.0
        )
        db.add(new_item)
        updated_items.append(new_item)

    bill.total_amount_calculated = total_calc
    bill.extraction_status = "VERIFIED"
    db.commit()

    return BillExtractionReviewResponse(
        bill_id=bill.id,
        hospital_name=bill.hospital_name,
        invoice_number=bill.invoice_number,
        bill_date=bill.bill_date,
        patient_identifier=bill.patient_identifier,
        total_claimed=bill.total_amount_claimed,
        total_calculated=bill.total_amount_calculated,
        line_items_count=len(updated_items),
        line_items=[BillLineItemSchema.model_validate(it) for it in updated_items],
        raw_ocr_preview=bill.original_ocr_text[:500] if bill.original_ocr_text else None
    )
