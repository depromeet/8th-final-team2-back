from rest_framework.serializers import ModelSerializer

from api.mission.serializers import MissionSerializer
from apps.article.models import Article, Comment, MediaContent, ArticleLike
from apps.user.models import User
from rest_framework import serializers


class MediaContentSerializer(ModelSerializer):
    class Meta:
        model = MediaContent
        fields = [
            "id",
            "file",
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "nickname",
            "image",
        ]


class ArticleSerializer(ModelSerializer):
    mission = MissionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "mission",
            "created_at",
            "user",
        ]


class ArticleCommentSerializer(ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    user_profile = serializers.SerializerMethodField()
    mission = MissionSerializer(read_only=True)

    def get_user_profile(self, obj):
        user = obj.user
        if user:
            return user.get_absolute_url
        return ""

    class Meta:
        model = Comment
        fields = ["id", "article", "user", "content", "user_profile", "mission"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "article",
            "user",
            "content",
        ]


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "article", "user", "content"]


class ArticleLikeSerializer(ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = [
            "id",
            "article",
            "user",
        ]


class ArticleWithCommentSerializer(ModelSerializer):
    media_contents = MediaContentSerializer(many=True, read_only=True)
    comments = ArticleCommentSerializer(many=True, read_only=True)
    article_likes = ArticleLikeSerializer(many=True, read_only=True)
    mission = MissionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "user",
            "media_contents",
            "article_likes",
            "comments",
            "created_at",
            "like_users",
            "mission",
        ]


class ArticleCreateSerializer(ModelSerializer):
    file_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    media_contents = MediaContentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "file_ids",
            "user",
            "media_contents",
            "mission",
        ]

    def create(self, validated_data):
        ids = validated_data.pop("file_ids")
        instance = super().create(validated_data)

        contents = MediaContent.objects.filter(id__in=ids)
        instance.media_contents.add(*contents)

        return instance


class ArticleWithCountSerializer(ModelSerializer):
    media_contents = MediaContentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    mission = MissionSerializer(read_only=True)

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "media_contents",
            "like_count",
            "comment_count",
            "created_at",
            "user",
            "mission",
        ]
