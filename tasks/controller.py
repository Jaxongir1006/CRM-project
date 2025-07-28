from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .schemas import (
    TaskSchema,
    MeetingSchema,
    CreateTaskSchema,
    CreateMeetingSchema,
    ErrorSchema,
    UpdateTaskSchema,
    UpdateMeetingSchema,
)
from .models import Task, Meeting
from ninja_extra.permissions import IsAuthenticated
from utils.permissions import IsAdminManagerSales
from ninja_jwt.authentication import JWTAuth
from typing import List
from customers.models import Customer


@api_controller("/tasks", auth=JWTAuth(), permissions=[IsAuthenticated], tags=["Tasks"])
class TaskController:
    @http_post(
        "/create/",
        permissions=[IsAdminManagerSales],
        response={201: TaskSchema, 400: ErrorSchema},
    )
    def create_task(self, request, data: CreateTaskSchema):
        user = request.user
        data = data.model_dump(exclude_unset=True)
        data.pop("assignee")
        data["assignee"] = user
        try:
            task = Task.objects.create(**data)
        except Exception as e:
            return 400, {"error": str(e)}
        return 201, task

    @http_get("/", response=List[TaskSchema])
    def get_tasks(self, request):
        return Task.objects.all()

    @http_get("/{task_id}/", response={200: TaskSchema, 404: ErrorSchema})
    def get_one_task(self, task_id, request):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return 404, {"error": "Task not found"}

        return task

    @http_put(
        "/update/{task_id}/",
        response={200: TaskSchema, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def update_task(self, task_id, request, data: UpdateTaskSchema):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return 404, {"error": "Task not found"}

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        task.save()
        return task

    @http_delete(
        "/delete/{task_id}/",
        response={200: dict, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def delete_task(self, task_id, request):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return 404, {"error": "Task not found"}
        task.delete()
        return 200, {"message": "The task has been deleted"}


@api_controller(
    "/meeting", auth=JWTAuth(), permissions=[IsAuthenticated], tags=["Meeting"]
)
class MeetingController:
    @http_post(
        "/create/",
        response={201: MeetingSchema, 400: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def create_task(self, request, data: CreateMeetingSchema):
        customer = Customer.objects.filter(id=data.customer).first()
        if not customer:
            return 400, {"error": "Customer not found"}
        data = data.model_dump(exclude_unset=True)
        data.pop("customer")
        data["customer"] = customer
        try:
            meeting = Meeting.objects.create(**data)
        except Exception as e:
            return 400, {"error", str(e)}

    @http_get("/", response=List[MeetingSchema])
    def get_meetings(self, request):
        return Meeting.objects.all()

    @http_get("/{meeting_id}/", response={200: MeetingSchema, 404: ErrorSchema})
    def get_one_meeting(self, meeting_id, request):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return 404, {"error": "Meeting not found"}
        return 200, meeting


    @http_put(
        "/update/{meeting_id}/",
        response={200: MeetingSchema, 404: ErrorSchema},
        permissions=[IsAdminManagerSales],
    )
    def update_meeting(self, meeting_id, request, data: UpdateMeetingSchema):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return 404, {"error":"Meeting with this id does not exist"}
         
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(meeting, key, value)
        meeting.save()

        return 200, meeting
    
    @http_delete("/delete/{meeting_id}/", response={200: dict, 404: ErrorSchema}, permissions=[IsAdminManagerSales])
    def delete_meeting(self, meeting_id, request):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return 404, {"error":"Meeting with this id does not exist"}
        
        meeting.delete()
        return 200, {"message":"The meeting has been deleted"}