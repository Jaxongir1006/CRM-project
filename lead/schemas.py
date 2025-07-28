from ninja import Schema, ModelSchema
from .models import Lead, Deal
from typing import Optional


class ErrorSchema(Schema):
    error: str


class LeadSchema(ModelSchema):
    class Config:
        model = Lead
        model_fields = ["id", "full_name", "email", "phone", "source", "status", "created_by"]
        from_attributes = True

class DealSchema(ModelSchema):
    class Config:
        model = Deal
        model_fields = ["id", "lead", "status", "amount", "close_date"]
        from_attributes = True


class CreateLeadSchema(Schema):
    full_name: str
    email: str
    phone: str
    source: str
    status: Optional[str] = "new"


class UpdateLeadSchema(Schema):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None    



class CreateDealSchema(Schema):
    lead: int
    status: Optional[str] = 'open'
    amount: float
    close_date: Optional[str] = None


class UpdateDealSchema(Schema):
    status: Optional[str] = "open"
    amount: Optional[float] = None
    close_date: Optional[str] = None


class CloseDealSchema(Schema):
    status: str