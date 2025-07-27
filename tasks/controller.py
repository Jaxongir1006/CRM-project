from ninja_extra import api_controller, http_get, http_post
from .schemas import TaskSchema, MeetingSchema, CreateTaskSchema, CreateMeetingSchema, ErrorSchema
from .models import Task, Meeting
from ninja_extra.permissions import IsAuthenticated
from utils.permissions import IsAdminManagerSales


