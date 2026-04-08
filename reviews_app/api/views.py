from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import Review
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.api.permissions import IsCustomerUser, IsReviewOwnerOrReadOnly
from reviews_app.api.filters import ReviewFilter


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter

    ordering_fields = ['updated_at', 'rating']
    ordering = ['-created_at']

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwnerOrReadOnly]