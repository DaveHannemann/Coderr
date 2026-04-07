from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessAndOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == 'DELETE':
            return request.user.is_staff

        if request.user.profile.type != 'business':
            return False

        return obj.business_user == request.user
    
class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.profile.type == 'customer'

        return True