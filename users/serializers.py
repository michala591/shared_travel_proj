from rest_framework import serializers
from .models import User


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"  # You can also specify fields explicitly if needed


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_type"]  # You can also specify fields explicitly if needed
