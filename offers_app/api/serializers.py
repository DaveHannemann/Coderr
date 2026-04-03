
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetail-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class OfferDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferFullDetailSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image', 'description',
            'details'
        ]


class OfferWriteSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, required=False)
    image = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate(self, data):
        details = data.get('details', None)

        if self.instance is None:
            if not details or len(details) != 3:
                if len(details) != 3:
                    raise serializers.ValidationError(
                        "You must provide exactly 3 offer details."
                    )

            types = [d.get('offer_type') for d in details]

            required_types = {'basic', 'standard', 'premium'}

            if set(types) != required_types:
                raise serializers.ValidationError(
                f"Offer must include exactly these types: {required_types}"
                )
        
        else:
            if details:
                for detail in details:
                    if 'offer_type' not in detail:
                        raise serializers.ValidationError(
                            "Each detail must include an 'offer_type'."
                        )

        return data

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')

                if not offer_type:
                    raise serializers.ValidationError(
                        "offer_type is required for updating details."
                    )

                try:
                    detail = instance.details.get(offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Detail with type '{offer_type}' does not exist."
                    )

                for attr, value in detail_data.items():
                    setattr(detail, attr, value)

                detail.save()

        return instance
    
class OfferReadSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username
        }
    
class OfferDetailReadSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]