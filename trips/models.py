from django.db import models

from cars.models import Car
from locations.models import Locations
from users.models import User


class Trips(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="trips")
    days = models.CharField(max_length=50)
    departure_time = models.TimeField()
    return_time = models.TimeField()
    origin_station = models.ForeignKey(
        Locations, on_delete=models.CASCADE, related_name="trips_origin"
    )
    destination_station = models.ForeignKey(
        Locations, on_delete=models.CASCADE, related_name="trips_destination"
    )
    users = models.ManyToManyField(User, related_name="trips")

    def __str__(self):
        return f"Trip by {self.users} from {self.origin_station} to {self.destination_station}"

    def passengers_count(self):
        return self.users.filter(is_enabled=True).count()

    def available_seats(self):
        return self.car.max_capacity - self.passengers_count()


class FrozenPassenger(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    freeze_until = models.DateTimeField()

    def __str__(self):
        return f"Frozen {self.user} in {self.trip} until {self.freeze_until}"
