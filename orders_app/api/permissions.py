from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessAndOwnerOrReadOnly(BasePermission):
    """
    Permission that allows:
        - Read access for everyone
        - Write access only for business users who own the order
        - Delete access only for admin users
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == 'DELETE':
            return request.user.is_staff

        if request.user.profile.type != 'business':
            return False

        return obj.business_user == request.user
    
class IsCustomerUser(BasePermission):
    """
    Permission that allows only customer users to create orders.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.profile.type == 'customer'

        return True