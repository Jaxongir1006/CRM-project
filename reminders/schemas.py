from ninja import Schema, ModelSchema
from .models import Reminder
from typing import Optional


class ErrorSchema(Schema):
    error : str



class ReminderSchema(ModelSchema):
    class Config:
        model = Reminder
        model_fields = ['id', 'user', 'customer', 'message', 'is_sent', 'remind_at']
        from_attributes = True

    

class CreateReminderSchema(Schema):
    customer_mail : Optional[str] = None
    message : str
    is_sent : Optional[str] = False
    remind_at : str


class UpdateReminderSchema(Schema):
    customer_mail : Optional[str] = None
    message : Optional[str] = None
    is_sent : Optional[str] = False
    remind_at : Optional[str] = None