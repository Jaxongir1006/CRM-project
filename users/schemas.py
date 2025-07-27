from ninja import Schema, ModelSchema
from .models import CustomUser
from typing import Optional

class CustomUserSchema(ModelSchema):
    class Config:
        model = CustomUser
        model_fields = ['username', 'email', 'role', 'is_active', 'phone_number']
        from_attributes = True


class RegistereSchema(Schema):
    username: str
    email: str
    password: str
    confirm_password: str
    phone_number: str
    role: Optional[str] = 'sales'

class LoginSchema(Schema):
    login_input: str
    password: str


class ErrorSchema(Schema):
    error: str

