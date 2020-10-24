from rest_framework import serializers

from apps.user.models import User
from apps.user.enums import Provider
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


class SocialSerializer(serializers.Serializer):
    authorization_code = serializers.CharField(
        label="인증코드", write_only=True, help_text="각 플랫폼에서 OAuth로 발급받은 AuthorizationCode를 넣어주세요")
    provider = serializers.ChoiceField(label="플랫폼", choices=Provider.choices)

    def save(self):
        pass
