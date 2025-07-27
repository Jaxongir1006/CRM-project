from django.contrib import admin
from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "type"]
    list_filter = ["type", 'customer', 'created_by']