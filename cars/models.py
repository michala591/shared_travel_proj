from django.db import models
from users.models import User


class Car(models.Model):
    license_plate = models.CharField(max_length=8, unique=True)
    model = models.CharField(max_length=50)
    max_capacity = models.IntegerField(default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")

    def __str__(self):
        return f"{self.model} ({self.license_plate})"
