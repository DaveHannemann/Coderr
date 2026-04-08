from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from reviews_app.models import Review


class ReviewFilter(filters.FilterSet):
    business_user = filters.NumberFilter(field_name='business_user__id')
    reviewer = filters.NumberFilter(field_name='customer_user__id')

    class Meta:
        model = Review
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        if data:
            extra_allowed = {'ordering'}
            allowed = set(self.filters.keys()) | extra_allowed
            received = set(data.keys())

            unknown = received - allowed

            if unknown:
                raise ValidationError({
                    "error": f"Ungültige Anfrageparameter: {', '.join(unknown)}"
                })