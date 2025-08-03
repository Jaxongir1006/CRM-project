from django.contrib import admin
from .models import Reminder




@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'remind_at', 'is_sent', 'id']
    list_filter = ['user', 'is_sent']
    