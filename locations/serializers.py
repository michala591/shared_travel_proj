from rest_framework import serializers
from .models import Locations


class locationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"  # You can also specify fields explicitly if needed


class locationsIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ["id"]  
