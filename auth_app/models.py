from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=255, blank=True, default='')
    type = models.CharField(max_length=50, choices=PROFILE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username