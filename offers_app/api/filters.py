from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from offers_app.models import Offer

class OfferFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='min_price', lookup_expr='lte')

    min_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')

    creator_id = filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Offer
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        if data:
            extra_allowed = {'page', 'ordering'}
            allowed = set(self.filters.keys()) | extra_allowed
            received = set(data.keys())

            unknown = received - allowed

            if unknown:
                raise ValidationError({
                    "error": f"Ungültige Anfrageparameter: {', '.join(unknown)}"
                })