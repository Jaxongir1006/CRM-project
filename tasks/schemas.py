from ninja import Schema, ModelSchema
from .models import Task, Meeting
from typing import Optional


class ErrorSchema(Schema):
    error: str


class TaskSchema(ModelSchema):
    class Config:
        model = Task
        model_fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'deadline', 'assignee']
        from_attributes = True

    
class MeetingSchema(ModelSchema):
    class Config:
        model = Meeting
        model_fields = ['id', 'customer', 'datetime', 'purpose', 'location', 'created_at', 'updated_at']
        from_attributes = True


class CreateTaskSchema(Schema):
    title: str
    deadline: str
    description: Optional[str] = None
    status: Optional[str] = "todo"


class CreateMeetingSchema(Schema):
    customer: int
    datetime: str
    purpose: str
    location: Optional[str]


class UpdateTaskSchema(Schema):
    title: Optional[str] = None
    deadline: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "todo"    


class UpdateMeetingSchema(Schema):
    customer: Optional[int] = None
    datetime: Optional[str] = None
    purpose: Optional[str] = None
    location: Optional[str] = None