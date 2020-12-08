from rest_framework import serializers
from drf_yasg import openapi


class PostImageRequest(serializers.Serializer):
    image = serializers.ImageField(label="이미지")
    priority = serializers.IntegerField(
        label="우선순위", required=False, default=0, help_text="숫자가 낮을수록 우선순위가 높습니다."
    )


post_image_request = PostImageRequest


class PostImageResponse(serializers.Serializer):
    id = serializers.IntegerField(label="이미지 일련번호", required=False)
    image = serializers.ImageField(label="이미지", required=False)
    priority = serializers.IntegerField(label="우선순위", required=False)


post_image_response = openapi.Response("", PostImageResponse)


class PostRequest(serializers.Serializer):
    mission = serializers.IntegerField(
        label="미션 일련번호", help_text="각 미션 카테고리마다 글을 작성하기 떄문에 미션 ID 값을 보내주시면 됩니다."
    )
    content = serializers.CharField(label="내용", required=False)
    images = serializers.ListField(
        label="이미지 일련번호 목록",
        required=False,
        child=serializers.IntegerField(label="이미지 일련번호"),
    )


post_request = PostRequest


class PostUserResponse(serializers.Serializer):
    nickname = serializers.CharField(label="닉네임")
    image: serializers.ImageField(label="유저 이미지")


class PostListResponse(serializers.Serializer):
    id = serializers.IntegerField(label="게시글 일련번호")
    images = serializers.ListField(label="이미지 목록", child=serializers.ImageField())
    contnet = serializers.CharField(label="내용")
    mission = serializers.CharField(label="미션 명")
    user = PostUserResponse()
    is_like = serializers.BooleanField(label="좋아요여부")
    favorite_count = serializers.IntegerField(label="좋아요 수")
    comment_count = serializers.IntegerField(label="댓글 수")
    created_at = serializers.DateTimeField(label="생성일")


post_list_response = openapi.Response("", PostListResponse(many=True))


class PostLikeRequest(serializers.Serializer):
    post = serializers.IntegerField(label="게시글 일련번호")
    is_like = serializers.BooleanField(label="좋아여 여부")


post_like_request = PostLikeRequest


class PostLikeResponse(serializers.Serializer):
    favorite_count = serializers.IntegerField(label="좋아요 수")
    is_like = serializers.BooleanField(label="좋아요 여부")


post_like_response = openapi.Response("", PostLikeResponse)


class PostDetailResponse(serializers.Serializer):
    id = serializers.IntegerField(label="게시글 일련번호")


post_detail_response = openapi.Response("", PostDetailResponse)


class CommentRequest(serializers.Serializer):
    pass


class CommentResponse(serializers.Serializer):
    pass


comment_request = CommentRequest


comment_create_response = openapi.Response("", CommentResponse)