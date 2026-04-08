from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.profile.type == 'customer'
        return True
    
class IsReviewOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.customer_user == request.user