# bot/models.py

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    zone = models.CharField(max_length=100, default="Zone 1")
    is_active = models.BooleanField(default=True)
    auto_booking_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.email
