from rest_framework import serializers

from cars.models import Car
from users.models import User
from locations.models import Locations
from .models import Trips


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"  # Add more fields as needed


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["max_capacity"]  # Add more fields as needed


class TripsLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ["city", "zone"]


class tripsSerializer(serializers.ModelSerializer):
    origin_station = TripsLocationsSerializer()
    destination_station = TripsLocationsSerializer()
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Trips
        fields = "__all__"

    def get_available_seats(self, obj):
        return obj.available_seats()


class TripsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trips
        fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "trips",
            "user_type",
            "is_active",
        ]  # Customize as needed


class TripsLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ["city", "zone"]


class SearchTripsSerializer(serializers.ModelSerializer):
    origin_station = TripsLocationsSerializer()
    destination_station = TripsLocationsSerializer()

    class Meta:
        model = Trips
        fields = [
            "days",
            "departure_time",
            "return_time",
            "origin_station",
            "destination_station",
        ]
