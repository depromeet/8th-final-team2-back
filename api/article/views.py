from django.http import HttpResponse
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator
 
from . import serializers
from apps.article.models import Article, ArticleLike, Comment, MediaContent
from . import pagination

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = serializers.ArticleSerializer
    permission_classes = [AllowAny]
    pagination_class = pagination.ArticlePagination

    def get_queryset(self):
        request = self.request
        self.queryset = self.queryset.annotate(like_count=Count("like_users"))

        return self.queryset

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.ArticleCreateSerializer
        if self.action == "retrieve":
            return serializers.ArticleWithCommentSerializer
        if self.action == "list":
            return serializers.ArticleWithCountSerializer
        return serializers.ArticleSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "create":
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_summary="게시글 리스트",
        operation_description="""
        게시글 리스트 API
        ---
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MediaContentViewSet(ModelViewSet):
    queryset = MediaContent.objects.all()
    serializer_class = serializers.MediaContentSerializer


class ArticleLikeViewSet(ModelViewSet):
    queryset = ArticleLike.objects.all()
    serializer_class = serializers.ArticleLikeSerializer

    def create(self, request):
        article_id = request.data["article"]
        user = request.data["user"]
        article = get_object_or_404(Article, pk=article_id)

        if article.like_users.filter(id=user):
            article.like_users.remove(user)
        else:
            article.like_users.add(user)

        return HttpResponse(status=200)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CommentCreateSerializer
        return serializers.CommentSerializer
