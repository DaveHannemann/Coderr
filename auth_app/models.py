from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(max_length=50, choices=PROFILE_TYPE_CHOICES)

    def __str__(self):
        return self.user.username