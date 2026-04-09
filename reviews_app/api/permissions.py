from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    """
    Permission that allows only customer users to create reviews.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.profile.type == 'customer'
        return True
    
class IsReviewOwnerOrReadOnly(BasePermission):
    """
    Permission that allows:
        - Read access for all authenticated users
        - Write access only for the review owner
    """
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.customer_user == request.user