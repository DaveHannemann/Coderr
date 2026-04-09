from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from reviews_app.models import Review


class ReviewFilter(filters.FilterSet):
    business_user_id = filters.NumberFilter(field_name='business_user__id')
    reviewer_id = filters.NumberFilter(field_name='customer_user__id')

    class Meta:
        model = Review
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        if data:
            data = data.copy()
            data = {k: v for k, v in data.items() if v not in ["", None]}
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