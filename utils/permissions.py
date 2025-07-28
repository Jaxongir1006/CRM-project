from ninja_extra.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, controller):
        return request.user.role == "admin"
    

class IsAdminManagerSales(BasePermission):
    def has_permission(self, request, controller) -> bool:
        return hasattr(request.user, "role") and request.user.role.lower() in ["admin", "manager", "sales"]
