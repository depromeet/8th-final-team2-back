from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from apps.user.enums import Provider
from apps.badge.models import ProfileIcon
from .oauth import Kakao


class ProfileIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIcon
        fields = ["id", "name", "image"]


class UserSerializer(serializers.ModelSerializer):
    profile_icons = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "image",
            "profile_icons"
        ]

    def get_profile_icons(self, obj):
        serializer = ProfileIconSerializer(
            instance=obj.userprofileicon_set.all(), many=True)
        return serializer.data


class SocialSerializer(serializers.Serializer):
    authorization_code = serializers.CharField(write_only=True)
    provider = serializers.ChoiceField(
        choices=Provider.choices, write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        code = attrs["authorization_code"]
        provider = attrs["provider"]

        user = None
        if provider == Provider.GOOGLE:
            pass
        elif provider == Provider.KAKAO:
            kakao = Kakao(token=code)
            user = kakao.get_user()

        if user is None:
            raise serializers.ValidationError(f"fail to login {provider}")

        refresh = RefreshToken.for_user(user)
        attrs["access_token"] = str(refresh.access_token)
        attrs["refresh_token"] = str(refresh)
        attrs["user"] = user

        return attrs


class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User is not existed")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Check username and password")

        attrs["user"] = user

        refresh = RefreshToken.for_user(user)
        attrs["access_token"] = str(refresh.access_token)
        attrs["refresh_token"] = str(refresh)

        return attrs
