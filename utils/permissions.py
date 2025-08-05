from ninja_extra.permissions import BasePermission
import logging

logger = logging.getLogger('__name__')

class IsAdmin(BasePermission):
    def has_permission(self, request, controller):
        return request.user.role == "admin"
    

class IsAdminManagerSales(BasePermission):
    def has_permission(self, request, controller) -> bool:
        if hasattr(request.user, "role") and request.user.role.lower() in ["admin", "manager", "sales"]:
            return True
        logger.error(f"{request.user} This user tried to do something without being sales, manager or admin")
        return False
