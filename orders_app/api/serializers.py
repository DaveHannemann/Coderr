from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail
from django.shortcuts import get_object_or_404


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for creating, retrieving, and updating orders.

    Input:
        offer_detail_id (int): ID of the selected OfferDetail

    Behavior:
        - On create:
            * Copies data from OfferDetail into Order (snapshot)
            * Assigns customer_user and business_user automatically
            * Prevents duplicate active orders for the same offer_detail

        - On update:
            * Only 'status' field can be updated
            * Only business users can update status
            * Enforces valid status transitions:
                - in_progress → completed or cancelled
                - completed/cancelled → no further changes

    Read-only:
        - All offer-related fields (title, price, etc.)
        - user fields
        - timestamps
    """
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
            'offer_detail_id'
        ]
        read_only_fields = [
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        offer_detail_id = validated_data.pop('offer_detail_id')

        if Order.objects.filter(
            customer_user=user,
            offer_detail_id=offer_detail_id,
            status='in_progress'
        ).exists():
            raise serializers.ValidationError(
                "You already have an active order for this offer."
            )

        detail = get_object_or_404(
            OfferDetail.objects.select_related('offer__user'),
            id=offer_detail_id
        )

        return Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=detail.offer.user,
            offer=detail.offer,
            offer_detail=detail,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )
    
    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        new_status = validated_data.get('status')

        allowed_fields = {'status'}
        incoming_fields = set(request.data.keys())

        if not incoming_fields.issubset(allowed_fields):
            raise serializers.ValidationError(
                f"Only these fields can be updated: {allowed_fields}"
            )

        VALID_TRANSITIONS = {
            'in_progress': ['completed', 'cancelled'],
            'completed': [],
            'cancelled': []
        }

        if new_status:
            if user.profile.type != 'business':
                raise serializers.ValidationError(
                    "Only business users can update status."
                )
            if new_status not in VALID_TRANSITIONS[instance.status]:
                raise serializers.ValidationError(
                    f"Cannot change status from {instance.status} to {new_status}."
                )

            instance.status = new_status
            instance.save()
        
        return instance