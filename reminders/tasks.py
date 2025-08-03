from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Reminder
from django.utils.timezone import now



@shared_task
def check_due_reminders():
    due_reminders = Reminder.objects.filter(is_sent=False, remind_at__lte=now())
    
    for reminder in due_reminders:
        customer = reminder.customer
        if not customer or not customer.email:
            continue

        subject = f"Eslatma: {customer.name} uchun"
        message = reminder.message
        to_email = customer.email
        from_email = settings.EMAIL_HOST_USER

        html_content = render_to_string('reminder.html', {
            "message": message,
            "customer_name": customer.name,
        })
        
        msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        print("jalab borgan bolishi kere zb boru")
        reminder.is_sent = True
        reminder.save()