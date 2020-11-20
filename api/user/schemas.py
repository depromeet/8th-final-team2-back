from django.db import models
from rest_framework import serializers
from rest_framework.serializers import Serializer
from drf_yasg.openapi import Response


class Provider(models.TextChoices):
    KAKAO = "kakao", "카카오"
    GOOGLE = "google", "구글"


class SocialRequest(Serializer):
    id_token = serializers.CharField(
        label="ID 토큰", help_text="플랫폼에서 OAuth로 발급받은 IdToken을 넣어주세요"
    )
    provider = serializers.ChoiceField(label="플랫폼", choices=Provider.choices)


social_request = SocialRequest


class LoginRequest(Serializer):
    username = serializers.CharField(label="아이디")
    password = serializers.CharField(label="비밀번호")


login_request = LoginRequest


class UserResponse(Serializer):
    id = serializers.IntegerField(label="일련번호", required=False)
    username = serializers.CharField(label="아이디", required=False)
    image = serializers.ImageField(label="이미지", required=False)
    nickname = serializers.CharField(label="닉네임", required=False)
    has_nickname = serializers.BooleanField(label="닉네임 작성여부", required=False)
    has_image = serializers.BooleanField(label="이미지 보유여부", required=False)


class LoginResponse(Serializer):
    access_token = serializers.CharField(label="AccessToken", required=False)
    refresh_token = serializers.CharField(label="RefreshToken", required=False)
    user = UserResponse(read_only=True, required=False)


login_response = Response("", LoginResponse)


class IconResponse(Serializer):
    name = serializers.CharField(label="아이콘명")
    image = serializers.CharField(label="아이콘명", help_text="획득 시에는 활성화된 이미지가 내려갑니다.")
    acquired_date = serializers.CharField(label="획득일", required=False, allow_null=True)
    is_active = serializers.BooleanField(label="획득여부")


class ProfileResponse(Serializer):
    nickname = serializers.CharField(label="닉네임", required=False)
    image = serializers.ImageField(label="프로필 이미지")
    complete_mission_count = serializers.IntegerField(label="달성한 미션수", required=False)
    post_count = serializers.IntegerField(label="게시물 수", required=False)
    experience = serializers.IntegerField(label="획득한 경험치", required=False)
    total_experience = serializers.IntegerField(label="전체 경험치", required=False)

    profile_icons = IconResponse(read_only=True, many=True)


profile_response = Response("", ProfileResponse)


class ProfileRequest(Serializer):
    nickname = serializers.CharField(label="닉네임")


profile_request = ProfileRequest


class ProfileImageRequest(Serializer):
    image = serializers.FileField(label="이미지")


profile_image_request = ProfileImageRequest