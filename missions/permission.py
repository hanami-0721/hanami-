from rest_framework.permissions import BasePermission

class IsPublisher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.publisher == request.user

class IsAcceptor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.acceptor == request.user

class IsPublisherOrAcceptorReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return obj.publisher == request.user or obj.acceptor == request.user
        return False

class IsPartAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_part_admin