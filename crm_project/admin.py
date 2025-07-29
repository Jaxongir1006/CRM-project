# from django.contrib.admin import AdminSite
# from django.template.response import TemplateResponse
# from django.urls import path
# from django.utils.timezone import now
# from users.models import CustomUser as User
# from lead.models import Lead
# from customers.models import Customer

# class CustomJazzminAdmin(AdminSite):
#     site_header = "CRM Dashboard"
#     site_title = "CRM Admin"
#     index_title = "Statistik Panel"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("", self.admin_view(self.custom_index), name="index"),
#         ]
#         return custom_urls + urls

#     def custom_index(self, request):
#         # Statistikalar
#         stats = {
#             "total_users": User.objects.count(),
#             "total_leads": Lead.objects.count(),
#             "new_leads_today": Lead.objects.filter(created_at__date=now().date()).count(),
#             "active_customers": Customer.objects.filter(status="active").count(),
#         }

#         # app_list ni olish (chapdagi model menyulari uchun)
#         app_list = self.get_app_list(request)

#         context = self.each_context(request)
#         context.update(stats)
#         context["app_list"] = app_list  # 🟢 bu chiziq muhim!

#         return TemplateResponse(request, "admin/index.html", context)


# custom_admin_site = CustomJazzminAdmin(name='customadmin')
