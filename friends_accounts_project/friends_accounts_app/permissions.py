from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class CustomAuthenticationPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail="You do not have permission to access this resource.", code=403)
        return True
