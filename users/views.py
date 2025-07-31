# views.py
from django.contrib.admin.sites import site
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.utils.timezone import now
from lead.models import Lead, Deal
from customers.models import Customer
from users.models import CustomUser as User
from tasks.models import Meeting, Task
from interaction.models import Interaction


@staff_member_required
def custom_admin_index(request):
    context = {
        **site.each_context(),
        "total_users": User.objects.count(),
        "total_leads": Lead.objects.count(),
        "new_leads_today": Lead.objects.filter(created_at__date=now().date()).count(),
        "active_customers": Customer.objects.filter(status="active").count(),
        "new_meetings_today": Meeting.objects.filter(datetime=now().date()).count(),
        "tasks_to_do":Task.objects.filter(status='todo').count(),
        "deals":Deal.objects.filter(status='open').count(),
        "interactions_today":Interaction.objects.filter(next_action_date=now().date()).count(),
    }
    return TemplateResponse(request, "admin/index.html", context)


def home(request):
    return TemplateResponse(request, '404.html')