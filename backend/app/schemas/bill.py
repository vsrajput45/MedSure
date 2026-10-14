from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class BillLineItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    line_number: int
    raw_description: str
    normalized_description: str
    category: str = "OTHER"
    matched_procedure_code: Optional[str] = None
    quantity: float = 1.0
    unit_price: float = 0.0
    line_total: float = 0.0
    extracted_line_total: float = 0.0
    is_package_component: bool = False
    ocr_confidence: float = 1.0
    user_edited: bool = False

class LineItemsUpdate(BaseModel):
    items: List[BillLineItemSchema]

class BillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    file_name: str
    file_size_bytes: int
    mime_type: str
    hospital_name: Optional[str] = None
    invoice_number: Optional[str] = None
    bill_date: Optional[datetime] = None
    patient_identifier: Optional[str] = None
    extraction_status: str
    total_amount_claimed: float
    total_amount_calculated: float
    is_demo_sample: bool
    created_at: datetime
    line_items: List[BillLineItemSchema] = []

class BillExtractionReviewResponse(BaseModel):
    bill_id: str
    hospital_name: Optional[str] = None
    invoice_number: Optional[str] = None
    bill_date: Optional[datetime] = None
    patient_identifier: Optional[str] = None
    total_claimed: float
    total_calculated: float
    line_items_count: int
    line_items: List[BillLineItemSchema]
    raw_ocr_preview: Optional[str] = None
