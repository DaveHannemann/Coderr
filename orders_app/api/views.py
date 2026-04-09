from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from orders_app.api.permissions import IsBusinessAndOwnerOrReadOnly, IsCustomerUser
from orders_app.models import Order
from orders_app.api.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating orders.

    Permissions:
        - Authenticated users only
        - Only customers can create orders

    GET:
        - Customers see their own orders
        - Business users see orders assigned to them
        - Results are ordered by newest first

    POST:
        - Creates a new order from an OfferDetail
        - Requires 'offer_detail_id'

    Response:
        - List of orders or created order object
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser]

    def get_queryset(self):
        user = self.request.user
        profile_type = user.profile.type

        if profile_type == 'customer':
            return Order.objects.filter(customer_user=user).order_by('-created_at')

        elif profile_type == 'business':
            return Order.objects.filter(business_user=user).order_by('-created_at')

        return Order.objects.none()

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting orders.

    Permissions:
        - Authenticated users only
        - Only business owner or admin can modify

    GET:
        - Retrieve a single order

    PATCH / PUT:
        - Only 'status' can be updated
        - Only business user can update status
        - Enforces valid status transitions

    DELETE:
        - Only admin users can delete orders

    Queryset:
        - Customers see their own orders
        - Business users see assigned orders
        - Admin sees all orders
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBusinessAndOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        profile_type = user.profile.type

        if profile_type == 'customer':
            return Order.objects.filter(customer_user=user)

        elif profile_type == 'business':
            return Order.objects.filter(business_user=user)

        return Order.objects.none()
    
class OrderCountView(APIView):
    """
    API endpoint for retrieving the number of active orders
    (status = 'in_progress') for a business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        # Ensure business user exists
        user = get_object_or_404(User, id=business_user_id)

        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        return Response({
            "order_count": count
        })


class CompletedOrderCountView(APIView):
    """
    API endpoint for retrieving the number of completed orders
    for a business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id)
        
        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()

        return Response({
            "completed_order_count": count
        })