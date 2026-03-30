from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User

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
    
class ProfileCheckView(APIView):
    pass