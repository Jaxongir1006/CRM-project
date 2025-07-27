from django.db import models
from utils.models import TimeStampedModel


class Task(TimeStampedModel):
    class StatusEnum(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    title = models.CharField(max_length=255)
    deadline = models.DateField()
    assignee = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=StatusEnum.choices, default=StatusEnum.TODO)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_at"]

class Meeting(TimeStampedModel):
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="meetings")
    datetime = models.DateTimeField()
    purpose = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.customer} - {self.datetime}"

    class Meta:
        ordering = ["-created_at"]