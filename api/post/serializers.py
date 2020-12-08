from rest_framework import serializers

from api.user.serializers import UserSerializer
from apps.user.models import User
from apps.post.models import Comment, Post, PostImage


class UserSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    image = serializers.ImageField()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image", "priority"]
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    post_images = serializers.SerializerMethodField(read_only=True)
    images = serializers.ListField(write_only=True)
    content = serializers.CharField()
    mission = serializers.CharField(source="mission.name")
    user = UserSerializer(read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), write_only=True
    )
    is_like = serializers.SerializerMethodField(read_only=True)
    favorite_count = serializers.IntegerField(
        source="postlike_set.count", read_only=True
    )
    comment_count = serializers.IntegerField(source="comment_set.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "images",
            "post_images",
            "content",
            "mission",
            "user",
            "is_like",
            "favorite_count",
            "comment_count",
            "created_at",
        ]

    def get_post_images(self, obj):
        post_images = obj.postimage_set.order_by("priority")
        return [post_image.image.url for post_image in post_images]

    def get_is_like(self, obj):
        user = self.context["request"].user
        if user and user.is_authenticated:
            return obj.postlike_set.filter(user=user).exists()
        return False

    def create(self, validated_data):
        images = validated_data.pop("images")
        mission = validated_data.pop("mission")

        validated_data["mission_id"] = mission["name"]

        post = Post.objects.create(**validated_data)
        PostImage.objects.filter(id__in=images).update(post_id=post.id)

        return post


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


class ChildCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]


class CommentSerializer(serializers.Serializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), write_only=True
    )
    user = serializers.SerializerMethodField(label="유저", read_only=True)
    id = serializers.IntegerField(label="일련번호", read_only=True)
    content = serializers.CharField(label="내용")
    parent = serializers.PrimaryKeyRelatedField(
        label="부모댓글 일련번호",
        queryset=Comment.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )
    comments = serializers.SerializerMethodField(label="대댓글", read_only=True)
    created_at = serializers.DateTimeField(label="생성일", read_only=True)

    def create(self, validated_data):
        post_id = self.context["post_id"]
        validated_data["post_id"] = post_id
        user = validated_data.pop("author")
        validated_data["user"] = user

        comment = Comment.objects.create(**validated_data)

        return comment

    def get_comments(self, obj):
        instance = Comment.objects.filter(parent_id=obj["id"]).prefetch_related("user")
        serializer = ChildCommentSerializer(instance=instance, many=True)
        return serializer.data

    def get_user(self, obj):
        user = User.objects.get(id=obj["user_id"])
        serializer = UserSerializer(instance=user)
        return serializer.data