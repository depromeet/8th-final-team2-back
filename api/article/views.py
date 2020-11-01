from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count

from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers
from apps.article.models import Article, ArticleLike, Comment, MediaContent
from api.article.serializers import (
    ArticleCreateSerializer,
    ArticleLikeSerializer,
    ArticleSerializer,
    ArticleWithCommentSerializer,
    ArticleWithCountSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    MediaContentSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        request = self.request
        self.queryset = self.queryset.annotate(like_count=Count('like_users'))


        return self.queryset


    def get_serializer_class(self):
        if self.action == "create":
            return ArticleCreateSerializer
        if self.action == "retrieve":
            return ArticleWithCommentSerializer
        if self.action == "list":
            return ArticleWithCountSerializer
        return ArticleSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]




class MediaContentViewSet(viewsets.ModelViewSet):
    queryset = MediaContent.objects.all()
    serializer_class = MediaContentSerializer


class ArticleLikeViewSet(viewsets.ModelViewSet):
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer

    def create(self, request):
        article_id = request.data["article"]
        user = request.data["user"]
        article = get_object_or_404(Article, pk=article_id)

        if article.like_users.filter(id=user):
            article.like_users.remove(user)
        else:
            article.like_users.add(user)

        return HttpResponse(status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        return CommentSerializer
