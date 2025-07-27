from django.contrib import admin
from .models import Task, Meeting


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "deadline", "assignee", "status"]
    list_filter = ["status", "assignee"]


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "datetime", "purpose", "location"]
    list_filter = ["customer", 'datetime']