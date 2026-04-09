"""
Serializers for user authentication and registration.

This module contains serializers used for:
- returning user information
- registering new users
- logging in users
- validating email addresses
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning basic user information.

    Fields:
        id (int): Unique identifier of the user
        email (str): Email address of the user
        username (str): Username of the user
    """
    user_id = serializers.IntegerField(source="id")
    username = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = ["user_id", "email", "username"]

class RegisterSerializer(serializers.Serializer):
    """
    Serializer used for registering a new user.

    Input fields:
        username (str): Username of the user
        email (str): Email address
        password (str): Password for the account
        repeated_password (str): Password confirmation

    After successful registration:
        - a new User object is created
        - a corresponding UserProfile is created
        - an authentication token is generated
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=UserProfile.PROFILE_TYPE_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        """
        Validate the registration data.

        Checks:
        - Password and repeated_password must match
        - Email address must not already exist in the database

        Args:
            data (dict): Incoming serializer data

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If validation fails
        """

        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("User already exists")

        return data

    def create(self, validated_data):
        """
        Create a new user account.

        Steps:
        1. Remove repeated_password from validated data
        2. Create a new Django User
        3. Create a UserProfile linked to the user
        4. Generate an authentication token

        Args:
            validated_data (dict): Validated serializer data

        Returns:
            dict: Token and basic user information
        """

        profile_type = validated_data.pop("type")
        validated_data.pop("repeated_password")
        full_name = validated_data.get("username", "")
        first_name, last_name = full_name.split(" ", 1) if " " in full_name else (full_name, "")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name,
        )

        UserProfile.objects.create(
            user=user,
            type=profile_type,
        )

        token = Token.objects.create(user=user)

        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }


class LoginSerializer(serializers.Serializer):
    """
    Serializer used for authenticating users.

    Input fields:
        username (str): User username
        password (str): User password

    On successful authentication:
        - the user is authenticated via Django's authenticate()
        - a token is retrieved

    Returns:
        dict: Token and user information
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate login credentials.

        Uses Django's authenticate function to verify the user.

        Args:
            data (dict): Incoming login data

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If credentials are invalid
        """

        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        self.user = user
        return data
    
    def create(self, validated_data):
        """
        Return authentication token for the user.

        If a token already exists it will be reused,
        otherwise a new token will be created.

        Args:
            validated_data (dict): Validated login data

        Returns:
            dict: Token and user information
        """
        user = self.user

        token, _ = Token.objects.get_or_create(user=user)

        return {
            "token": token.key,
            "username": user.username,
            "user_id": user.id,
            "email": user.email,
        }

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for full user profile representation and update.

    Includes:
        - User-related fields (username, email, first_name, last_name)
        - Profile-specific fields (file, location, etc.)
        - Allows partial updates (PATCH)
        - Handles file uploads

    Validation:
        - Ensures email uniqueness across users

    Update:
        - Updates UserProfile fields
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    email = serializers.EmailField(source="user.email", required=False)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "username", "type", "created_at"]

    def validate(self, attrs):
        user_data = attrs.get("user", {})
        email = user_data.get("email")

        if email and self.instance:
            if User.objects.filter(email=email).exclude(pk=self.instance.user_id).exists():
                raise serializers.ValidationError({"email": "User already exists"})

        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance


class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public business profile representation.

    Includes only public-facing fields:
        - No email
        - No timestamps
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public customer profile representation.

    Includes minimal profile data.
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    file = serializers.FileField(required=False, allow_null=True)
    uploaded_at = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type",
        ]