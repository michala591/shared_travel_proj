from rest_framework import serializers

from users.models import User
from .models import Car


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name"]  # Add more fields as needed


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Car
        fields = "__all__"


class CarIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ["id"]
