from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPartAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_part_admin

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user