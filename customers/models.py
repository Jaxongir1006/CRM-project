from django.db import models
from utils.models import TimeStampedModel


class Customer(TimeStampedModel):
    class StatusEnum(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = "inactive", "Inactive"
        POTENTIAL = "potential", "Potential"
        CLOSED = "closed", "Closed"

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    lead = models.OneToOneField("lead.Lead", on_delete=models.CASCADE, related_name="customer", null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=StatusEnum.choices, default=StatusEnum.ACTIVE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_at']