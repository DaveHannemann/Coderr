from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Model representing a review from a customer to a business user.
    Each customer can leave only one review per business user.

    Constraints:
        - A customer can review a business only once
    """

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer_user', 'business_user'],
                name='unique_review_per_user_business'
            )
        ]

    def __str__(self):
        return f"Review #{self.id} - {self.description}"