from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apps.user.models import User
from . import serializers, schemas


class SocialAPIView(GenericAPIView):
    serializer_class = serializers.SocialSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="소설 로그인",
        operation_description="""
        소셜 로그인 API
        ---
        클라이언트에서 발급받은 access_token을 서버에 넘겨주면 서버에서 검증 후 로그인 처리.
        """,
        request_body=schemas.social_request,
        responses={status.HTTP_200_OK: schemas.login_response},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class LoginAPIView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="일반 로그인",
        operation_description="""
        로그인 API
        ---
        앱에서는 사용하는 것이 아니고 테스트 목적으로 만들어졌으며,
        응답은 소셜 로그인과 동일합니다.
        """,
        request_body=schemas.login_request,
        responses={status.HTTP_200_OK: schemas.login_response},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ProfileAPIView(GenericAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(id=self.request.user.id)
            .prefetch_related("userprofileicon_set")
        )

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get()
        except:
            return Http404
        return obj

    @swagger_auto_schema(
        operation_summary="프로필 조회",
        operation_description="""
        프로필 조회 API
        ---
        """,
        responses={status.HTTP_200_OK: schemas.profile_response},
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="프로필 수정",
        operation_description="""
        프로필 수정 API
        ---
        """,
        request_body=schemas.profile_request,
        responses={status.HTTP_200_OK: schemas.profile_response},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=self.get_queryset().get(), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ProfileImageAPIView(GenericAPIView):
    serializer_class = serializers.ProfileImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="프로필 이미지 수정",
        operation_description="""
        프로필 이미지 수정 API
        ---
        """,
        request_body=schemas.profile_image_request,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()