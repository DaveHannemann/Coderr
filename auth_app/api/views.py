

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from auth_app.models import UserProfile
from rest_framework.parsers import MultiPartParser, FormParser

class RegisterView(APIView):
    """
    API endpoint for user registration.

    Permissions:
        AllowAny

    Request Body:
        fullname (str)
        email (str)
        password (str)
        repeated_password (str)

    Response:
        token (str)
        fullname (str)
        email (str)
        id (int)
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Create a new user account.

        Returns authentication token and user information
        if registration is successful.
        """

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=201)

        return Response(serializer.errors, status=400)
    

class LoginView(APIView):
    """
    API endpoint for user authentication.

    Permissions:
        AllowAny

    Request Body:
        email (str)
        password (str)

    Returns:
        authentication token and user information.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate a user and return a token.
        """

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            return Response(data)

        return Response(serializer.errors, status=400)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, user_id=None):
        queryset = UserProfile.objects.select_related("user")

        if user_id:
            profile = get_object_or_404(queryset, user_id=user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        url_name = request.resolver_match.url_name

        if url_name == "business_profiles":
            queryset = queryset.filter(type="business")
            serializer = BusinessProfileSerializer(queryset, many=True)

        elif url_name == "customer_profiles":
            queryset = queryset.filter(type="customer")
            serializer = CustomerProfileSerializer(queryset, many=True)

        else:
            serializer = ProfileSerializer(queryset, many=True)

        return Response(serializer.data)

    def patch(self, request, user_id=None):
        profile = get_object_or_404(UserProfile.objects.select_related("user"), user_id=user_id)

        if request.user.id != profile.user_id:
            return Response(
                {"detail": "You do not have permission to edit this profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(ProfileSerializer(profile).data)