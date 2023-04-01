import json

from django.contrib.auth import authenticate, login
from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, write_only="True")
    password = serializers.CharField(max_length=100, write_only="True")

    def create(self, validated_data):
        user = authenticate(username=validated_data["username"], password=validated_data["password"])
        if not user:
            raise Exception("Invalid User")
        login(self.context.get("request"), user)
        return user