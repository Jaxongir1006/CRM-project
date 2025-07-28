from django.db import models
from utils.models import TimeStampedModel
from ninja.errors import ValidationError

class Lead(TimeStampedModel):
    class StatusEnum(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        LOST = "lost", "Lost"
        CONVERTED = "converted", "Converted"

    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=255)  # e.g. Instagram, website, referral
    status = models.CharField(max_length=20, choices=StatusEnum.choices, default=StatusEnum.NEW)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["phone", "created_by"],
                name="unique_lead_by_phone_and_creator"
            )
        ]

    def __str__(self):
        return f"{self.full_name} - {self.status}"
    
    def clean(self):
        if Lead.objects.exclude(id=self.id).filter(phone=self.phone, created_by=self.created_by).exists():
            raise ValidationError("This lead already exists for this user.")



class Deal(TimeStampedModel):
    class StatusEnum(models.TextChoices):
        OPEN = "open", "Open"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="deals")
    status = models.CharField(max_length=5, choices=StatusEnum.choices, default=StatusEnum.OPEN)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    close_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ["-created_at"]