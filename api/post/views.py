from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from apps.article.models import Post, Comment
from . import pagination, serializers, schemas


class PostViewSet(ModelViewSet):
    queryset = (
        Post.objects.all()
        .annotate(like_count=Count("like"))
        .order_by("-created_at")
        .prefetch_related("postimage_set")
        .prefetch_related("postlike_set")
        .prefetch_related("comment_set")
    )
    pagination_class = pagination.ArticlePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ArticleWithCommentSerializer
        elif self.action == "list":
            return serializers.PostListSerializer
        return serializers.PostSerializer

    @swagger_auto_schema(
        operation_summary="게시글 리스트",
        operation_description="""
        게시글 리스트 API
        ---
        미션별로 보시고자 할 경우에는 url query로 mission id 값을 넘겨주시면 됩니다.
        """,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="""
        게시글 생성 API
        ---
        이미지 포함 시 먼저 게시글 이미지 생성 API를 이용하여 업로드 후 이미지 id 값들을 Array 로 넘겨주세요
        """,
        request_body=schemas.post_request,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PostImageAPIView(CreateAPIView):
    serializer_class = serializers.PostImageSerializer
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        operation_summary="게시글 이미지 생성",
        operation_description="""
        게시글 이미지 생성 API
        ---
        게시글 생성 전에 이미지를 먼저 올려주시고, 반환되는 게시글 이미지 ID 값을 게시글 생성 때 같이 넘겨주시면 됩니다.
        """,
        request_body=schemas.post_image_request,
        responses={status.HTTP_200_OK: schemas.post_image_response},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PostLikeAPIView(GenericAPIView):
    serializer_class = serializers.PostLikeSerializer

    @swagger_auto_schema(
        operation_summary="게시글 좋아요",
        operation_description="""
        게시글 좋아요 API
        ---
        """,
        request_body=schemas.post_like_request,
        responses={status.HTTP_200_OK: schemas.post_like_response},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CommentCreateSerializer
        return serializers.CommentSerializer
