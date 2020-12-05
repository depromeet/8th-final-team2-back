from rest_framework import serializers

from api.mission.serializers import MissionSerializer
from api.user.serializers import UserSerializer
from apps.post.models import Comment, Post, PostImage, PostLike
from apps.mission.models import Mission


class UserSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    image = serializers.ImageField()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image", "priority"]
        read_only_fields = ["id"]


class PostSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mission = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all())
    content = serializers.CharField()
    images = serializers.ListField(
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=PostImage.objects.all()),
    )

    def create(self, validated_data):
        images = validated_data.pop("images")
        post = Post.objects.create(**validated_data)

        for image in images:
            image.post = post
        PostImage.objects.bulk_update(images, ["post"])

        return post


class PostListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    content = serializers.CharField()
    mission = serializers.CharField(source="mission.name")
    user = UserSerializer(read_only=True)
    favorite_count = serializers.IntegerField(source="postlike_set.count")
    comment_count = serializers.IntegerField(source="comment_set.count")

    class Meta:
        model = Post
        fields = [
            "id",
            "images",
            "content",
            "mission",
            "user",
            "favorite_count",
            "comment_count",
            "created_at",
        ]

    def get_images(self, obj):
        post_images = obj.postimage_set.order_by("priority")
        return [post_image.image.url for post_image in post_images]


class PostLikeSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True
    )
    is_like = serializers.BooleanField()
    favorite_count = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        user = attrs["user"]
        post = attrs["post"]
        is_like = attrs["is_like"]

        if is_like:
            post.like.add(user)
        else:
            post.like.remove(user)

        attrs.update({"favorite_count": post.postlike_set.count()})

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "content",
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "user", "content"]


class PostCommentSerializer(serializers.ModelSerializer):
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
        fields = [
            "id",
            "post",
            "user",
            "content",
            "user_profile",
            "mission",
        ]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = [
            "id",
            "post",
            "user",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    file_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "file_ids",
            "user",
            "mission",
        ]

    def create(self, validated_data):
        ids = validated_data.pop("file_ids")
        instance = super().create(validated_data)
        contents = PostImage.objects.filter(id__in=ids)
        instance.media_contents.add(*contents)

        return instance
