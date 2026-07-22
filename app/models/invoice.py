from datetime import date

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    invoice_id: str
    vendor_id: str
    po_number: str | None = None
    invoice_amount: float = Field(gt=0)
    currency: str
    invoice_date: date


class PurchaseOrder(BaseModel):
    po_number: str
    vendor_id: str
    po_amount: float = Field(gt=0)
    currency: str
    status: str


class Vendor(BaseModel):
    vendor_id: str
    vendor_name: str
    risk_level: str
    bank_change_pending: bool
    active: bool
