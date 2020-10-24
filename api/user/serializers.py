from rest_framework import serializers

from apps.user.models import User
from apps.badge.models import ProfileIcon


class ProfileIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIcon
        fields = ["id", "name", "image"]


class UserSerializer(serializers.ModelSerializer):
    profile_icons = ProfileIconSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "image",
            "profile_icons"
        ]
