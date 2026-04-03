
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBusinessUserOrReadOnly(BasePermission):
    message = "You must be a business user to create an offer."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not hasattr(user, 'profile'):
            return False

        return user.profile.type == 'business'
    
class IsAuthenticatedAndOwnerOrAdmin(BasePermission):
    message = "You must be the owner or an admin to modify this offer."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.user == request.user