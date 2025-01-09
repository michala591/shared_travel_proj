from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"  # You can also specify fields explicitly if needed


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_type"]  # You can also specify fields explicitly if needed


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)

        token["user_type"] = user.user_type
        token["name"] = user.name
        return token
