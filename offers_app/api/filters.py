from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from offers_app.models import Offer

class OfferFilter(filters.FilterSet):
    """
    FilterSet for filtering Offer queryset.

    Behavior:
        - Ignores empty query parameters
        - Raises ValidationError for unknown parameters

    Allowed query params:
        - All defined filters
        - page (pagination)
        - ordering (sorting)
        - search (if SearchFilter is used in the view)
        - page_size (if pagination is used in the view)
    """
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='min_price', lookup_expr='lte')

    min_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')

    creator_id = filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Offer
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        if data:
            data = data.copy()
            data = {k: v for k, v in data.items() if v not in ["", None]}
        super().__init__(data, *args, **kwargs)

        if data:
            extra_allowed = {'page_size', 'ordering', 'search', 'page'}
            allowed = set(self.filters.keys()) | extra_allowed
            received = set(data.keys())

            # Validate query parameters:
            # - Allow only defined filters + pagination + ordering
            # - Reject unknown parameters to prevent unintended filtering or misuse
            unknown = received - allowed

            if unknown:
                raise ValidationError({
                    "error": f"Unknown parameters: {', '.join(unknown)}"
                })