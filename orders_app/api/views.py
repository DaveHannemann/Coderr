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
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id)

        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        return Response({
            "order_count": count
        })


class CompletedOrderCountView(APIView):
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