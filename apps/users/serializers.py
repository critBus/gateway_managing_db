from crum import get_current_request
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import User


class UserSerializerRepresentation(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, value):
        request = get_current_request()
        return UserSerializerRepresentation(value, context={"request": request}).data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

    def to_representation(self, value):
        request = get_current_request()
        return UserSerializerRepresentation(value, context={"request": request}).data


class TokenAccesBlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField(allow_blank=False)
