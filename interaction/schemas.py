from ninja import Schema, ModelSchema
from .models import Interaction
from typing import Optional


class ErrorSchema(Schema):
    error: str


class InteractionSchema(ModelSchema):
    class Config:
        model = Interaction
        model_fields = ['id', 'customer', 'type', 'notes', 'date', 'created_by', 'next_action_date']
        from_attributes = True

class CreateInteractionSchema(Schema):
    customer: int
    type: str
    notes: Optional[str]
    date: Optional[str]
    created_by: Optional[int] = None
    next_action_date: Optional[str] = None


class UpdateInteractionSchema(Schema):
    customer: Optional[int] = None
    type: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[str] = None
    created_by: Optional[int] = None
    next_action_date: Optional[str] = None