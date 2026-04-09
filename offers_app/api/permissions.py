
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBusinessUserOrReadOnly(BasePermission):
    """
    Permission that allows read-only access for all users,
    but restricts write operations to authenticated business users.

    Rules:
        - SAFE_METHODS (GET, HEAD, OPTIONS): allowed for everyone
        - POST/PUT/PATCH/DELETE:
            * User must be authenticated
            * User must have a profile
            * Profile type must be "business"
    """
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
    """
    Permission that allows access only to authenticated users,
    and restricts modification to the object owner or admin.

    Rules:
        - All requests require authentication
        - SAFE_METHODS: allowed for authenticated users
        - Write operations:
            * Allowed for object owner
            * Allowed for admin (staff or superuser)
    """
    message = "You must be the owner or an admin to modify this offer."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.user == request.user