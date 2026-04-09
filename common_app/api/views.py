from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import UserProfile

from django.db.models import Avg


class BaseInfoView(APIView):
    """
    API endpoint for retrieving general platform statistics.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({
            "review_count": Review.objects.count(),
            "average_rating": round(
                Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0, 1
            ),
            "business_profile_count": UserProfile.objects.filter(type='business').count(),
            "offer_count": Offer.objects.count(),
        })