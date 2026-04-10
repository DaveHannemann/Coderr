from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from offers_app.api.filters import OfferFilter
from offers_app.api.pagination import CustomPagination
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferDetailReadSerializer, OfferReadSerializer, OfferWriteSerializer, OfferDetailSerializer, OfferFullDetailSerializer
from django.db.models import Min
from .permissions import IsBusinessUserOrReadOnly, IsAuthenticatedAndOwnerOrAdmin


class OfferListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating offers.

    Permissions:
        GET: AllowAny
        POST: Authenticated users with business profile only

    GET:
        - Returns paginated list of offers
        - Supports filtering, search, and ordering

    Filters:
        - Custom filters via OfferFilter
        - Search by title and description
        - Ordering by min_price and updated_at

    POST:
        - Creates a new offer with exactly 3 pricing tiers
        - Automatically assigns the current user as owner

    Response:
        - GET: List of offers (OfferReadSerializer)
        - POST: Created offer
    """
    queryset = Offer.objects.prefetch_related('details').annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    )
    permission_classes = [IsAuthenticatedOrReadOnly, IsBusinessUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['min_price', 'updated_at']
    ordering = ['-updated_at']
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferWriteSerializer
        return OfferReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a single offer.

    Permissions:
        - Only the owner or admin can modify

    Response:
        - GET: OfferDetailReadSerializer
        - UPDATE: OfferFullDetailSerializer (full nested data)
    """
    queryset = Offer.objects.prefetch_related('details').annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    )
    serializer_class = OfferDetailReadSerializer
    permission_classes = [IsAuthenticatedAndOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return OfferDetailReadSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return OfferWriteSerializer
        return OfferFullDetailSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = Offer.objects.prefetch_related('details').annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        ).get(pk=instance.pk)

        read_serializer = OfferFullDetailSerializer(instance, context={'request': request})
        return Response(read_serializer.data)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for managing individual OfferDetail objects.

    Permissions:
        - Only the owner or admin can modify
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticatedAndOwnerOrAdmin]
