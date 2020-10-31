from rest_framework import serializers
from rest_framework.serializers import Serializer
from drf_yasg.openapi import Response

from apps.user.enums import Provider


class UserResponseSerializer(Serializer):
    id = serializers.IntegerField(label="일련번호", required=False)
    username = serializers.CharField(label="아이디", required=False)
    nickname = serializers.CharField(label="닉네임", required=False)


class SocialRequestSerializer(Serializer):
    authorization_code = serializers.CharField(
        label="인증코드", help_text=" 플랫폼에서 OAuth로 발급받은 AuthorizationCode를 넣어주세요")
    provider = serializers.ChoiceField(label="플랫폼", choices=Provider.choices)


class LoginRequestSerializer(Serializer):
    username = serializers.CharField(label="아이디")
    password = serializers.CharField(label="비밀번호")


class LoginResponseSerializer(Serializer):
    access_token = serializers.CharField(label="AccessToken", required=False)
    refresh_token = serializers.CharField(label="RefreshToken", required=False)
    user = UserResponseSerializer(read_only=True, required=False)


login_request = LoginRequestSerializer
login_response = Response("", LoginResponseSerializer)
