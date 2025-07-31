from django.db import models
from utils.models import TimeStampedModel


class Reminder(TimeStampedModel):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reminders')
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, related_name='reminders', blank=True, null=True)
    message = models.TextField()
    remind_at = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} -> {self.message[:20]}'
    