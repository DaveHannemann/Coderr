from rest_framework import serializers
from reviews_app.models import Review
from orders_app.models import Order
from rest_framework.exceptions import PermissionDenied


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for creating, retrieving, and updating reviews.

    Behavior:
        - Automatically assigns the authenticated user as reviewer
        - Prevents users from reviewing themselves
        - Allows reviews only if a prior order exists between users
        - Ensures only one review per customer-business pair

    Validation:
        - Rating must be between 1 and 5
        - User must have placed an order with the business
        - Duplicate reviews are not allowed
    """
    reviewer = serializers.PrimaryKeyRelatedField(
        source='customer_user',
        read_only=True
    )
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'reviewer',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        business_user = validated_data.get('business_user')

        if business_user == user:
            raise serializers.ValidationError(
                "You cannot review yourself."
            )

        has_order = Order.objects.filter(
            customer_user=user,
            business_user=business_user
        ).exists()

        if not has_order:
            raise serializers.ValidationError(
                "You can only review businesses you have interacted with."
            )

        if Review.objects.filter(
            customer_user=user,
            business_user=business_user
        ).exists():
            raise PermissionDenied(
                "You have already reviewed this business."
            )

        return Review.objects.create(
            customer_user=user,
            **validated_data
        )