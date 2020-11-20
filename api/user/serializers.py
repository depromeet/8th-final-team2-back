from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from apps.user.enums import Provider
from apps.badge.models import ProfileIcon
from .oauth import Kakao, Google


class IconSerializer(serializers.Serializer):
    name = serializers.CharField()
    image = serializers.CharField()
    acquired_date = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):
    profile_icons = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "image",
            "nickname",
            "profile_icons",
            "has_nickname",
            "has_image",
        ]

    def get_profile_icons(self, obj):
        serializer = IconSerializer(instance=obj.userprofileicon_set.all(), many=True)
        return serializer.data


class SocialSerializer(serializers.Serializer):
    id_token = serializers.CharField(write_only=True)
    provider = serializers.ChoiceField(choices=Provider.choices, write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        id_token = attrs["id_token"]
        provider = attrs["provider"]

        user = None
        if provider == Provider.GOOGLE:
            google = Google(token=id_token)
            user = google.get_user()
        elif provider == Provider.KAKAO:
            kakao = Kakao(token=id_token)
            user = kakao.get_user()

        if user is None:
            raise serializers.ValidationError(f"fail to login {provider}")

        refresh = RefreshToken.for_user(user)
        attrs["access_token"] = str(refresh.access_token)
        attrs["refresh_token"] = str(refresh)
        attrs["user"] = user

        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

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


class ProfileSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    image = serializers.ImageField(read_only=True)
    profile_icons = serializers.SerializerMethodField(read_only=True)
    complete_mission_count = serializers.IntegerField(read_only=True, default=0)
    post_count = serializers.IntegerField(read_only=True, default=0)
    experience = serializers.IntegerField(read_only=True, default=0)
    total_experience = serializers.IntegerField(read_only=True, default=0)

    def get_profile_icons(self, obj):
        request = self.context["request"]
        user_data = obj.userprofileicon_set.all().values("id", "acquired_date")
        icon_data = [
            {
                "id": icon.id,
                "name": icon.name,
                "image": request.build_absolute_uri(icon.image.url),
                "active_image": request.build_absolute_uri(icon.active_image.url),
                "is_active": False,
            }
            for icon in (ProfileIcon.objects.all().order_by("priority"))
        ]
        print(icon_data)

        data = []
        for icon in icon_data:
            ud = next((u for u in user_data if u["id"] == icon["id"]), None)

            if ud is not None:
                icon.update(
                    {
                        "image": icon["active_image"],
                        "acquired_date": datetime.strftime(
                            ud["acquired_date"], "%Y.%m.%d"
                        ),
                        "is_active": True,
                    }
                )

            data.append(icon)

        return IconSerializer(instance=data, many=True).data

    def save(self):
        nickname = self.validated_data["nickname"]
        instance = self.instance
        instance.nickname = nickname
        instance.save()


class ProfileImageSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.FileField()

    def save(self):
        user = self.validated_data["user"]
        image = self.validated_data["image"]

        user.image = image
        user.save()
