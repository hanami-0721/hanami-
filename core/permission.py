from rest_framework.permissions import BasePermission

class IsPartAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_part_admin