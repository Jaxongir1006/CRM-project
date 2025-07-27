from django.contrib import admin
from .models import Lead,Deal


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'status']
    list_filter = ['status']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'lead', 'status']
    list_filter = ['status']