from ninja_extra.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, controller):
        return super().has_permission(request, controller) and request.user.role == "admin"
    

class IsAdminManagerSales(BasePermission):
    def has_permission(self, request, controller):
        return super().has_permission(request, controller) and request.user.role in ["admin", "manager", "sales"]
    
