from ninja import Schema, ModelSchema
from .models import Customer
from typing import Optional



class ErrorSchema(Schema):
    error: str


class CustomerSchema(ModelSchema):
    class Config:
        model = Customer
        model_fields = ['id', 'name', 'email', 'phone', 'status', 'address']
        from_attributes = True


class CreateCustomerSchema(Schema):
    name: str
    email: str
    phone: str
    address: str
    status: Optional[str] = "active"


class UpdateCustomerSchema(Schema):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None