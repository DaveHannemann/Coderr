from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    """
    Model representing a business user-created offer.

    Each offer belongs to a business user and can contain multiple pricing tiers
    via related OfferDetail objects.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class OfferDetail(models.Model):
    """
    Model representing a pricing tier for an offer.

    Each offer must contain exactly three detail types:
        - basic
        - standard
        - premium
    """
    OFFER_TYPE_CHOICES = (
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    )

    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(blank=True, default=list)
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.offer.title} - {self.title}"