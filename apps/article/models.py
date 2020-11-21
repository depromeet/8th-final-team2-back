from django.db import models

from utils.model import BaseModel
from .images import path_post_image


class Post(BaseModel):
    mission = models.ForeignKey("mission.Mission", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    content = models.TextField("내용", null=True, blank=True)
    like = models.ManyToManyField(
        "user.User", through="article.PostLike", related_name="like_users"
    )

    class Meta:
        db_table = "post"
        verbose_name = "글"
        verbose_name_plural = "글 목록"


class PostImage(BaseModel):
    post = models.ForeignKey("article.Post", on_delete=models.CASCADE)
    image = models.ImageField("이미지", upload_to=path_post_image)
    priority = models.IntegerField("우선순위", default=0)

    class Meta:
        db_table = "post_image"
        verbose_name = "글 이미지"
        verbose_name_plural = "글 이미지 목록"


class PostLike(BaseModel):
    article = models.ForeignKey("article.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "post_like"
        verbose_name = "글 좋아요"
        verbose_name_plural = "글 좋아요 목록"


class Comment(BaseModel):
    post = models.ForeignKey("article.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    comment = models.ForeignKey("self", on_delete=models.CASCADE)
    content = models.CharField("내용", max_length=100)

    class Meta:
        db_table = "post_comment"
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
