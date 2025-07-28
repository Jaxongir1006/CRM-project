from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from customers.models import Customer

@receiver(post_save, sender=Lead)
def create_customer_from_converted_lead(sender, instance, created, **kwargs):
    if not created and instance.status == Lead.StatusEnum.CONVERTED:
        try:
            instance.customer
            return
        except Customer.DoesNotExist:
            pass
        Customer.objects.create(
            name=instance.full_name,
            phone=instance.phone,
            email=instance.email,
            user=instance.created_by,
            lead=instance,
        )