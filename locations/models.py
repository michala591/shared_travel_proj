from django.db import models


class Locations(models.Model):
    city = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.zone}"
