from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.TextChoices):
    DRIVER = "DR", "Driver"
    PASSENGER = "PA", "Passenger"


class User(AbstractUser):
    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
    )
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # Better suited for phone numbers
    email = models.EmailField(unique=True)  # Use EmailField for validation
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"
