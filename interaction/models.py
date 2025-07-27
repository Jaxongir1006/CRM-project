from django.db import models
from utils.models import TimeStampedModel


class Interaction(TimeStampedModel):
    class TypeEnum(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        MEETING = "meeting", "Meeting"
        SUPPORT_TICKET = "support_ticket", "Support Ticket"

    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="interactions")
    type = models.CharField(max_length=15, choices=TypeEnum.choices, default=TypeEnum.CALL)
    notes = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    next_action_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} - {self.type}"
    
    class Meta:
        ordering = ["-created_at"]