from rest_framework import permissions
from .models import User

class IsManagerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and bool(request.user.is_manager or request.user.is_admin))
        

class IsOwnerPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)