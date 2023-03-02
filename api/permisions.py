from rest_framework import permissions

from account.models import User

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
     
        return obj.user == request.user or request.user.is_superuser
    

class IsHead(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
     
        return request.user.role == User.HEAD or request.user.is_superuser
    
    
class IsStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
     
        return request.user.role == User.STAFF or request.user.is_superuser

