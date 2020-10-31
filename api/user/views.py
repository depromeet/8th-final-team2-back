from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from . import serializers


class SocialAPIView(GenericAPIView):
    serializer_class = serializers.SocialSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="소설 로그인",
        operation_description="""
        소셜 로그인 API
        ---
        """
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class LoginAPIView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="일반 로그인", operation_description="""
        로그인 API
        ---
    """)
    def post(self, request, *args, **kwargs):
        return Response()
