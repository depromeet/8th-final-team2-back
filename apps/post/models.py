from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from utils.model import BaseModel
from .images import path_post_image


class Post(BaseModel):
    mission = models.ForeignKey("mission.Mission", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    content = models.TextField("내용", null=True, blank=True)
    like = models.ManyToManyField(
        "user.User", through="post.PostLike", related_name="like_users"
    )

    class Meta:
        db_table = "post"
        verbose_name = "글"
        verbose_name_plural = "글 목록"


class PostImage(BaseModel):
    post = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, null=True, blank=True
    )
    image = models.ImageField("이미지", upload_to=path_post_image)
    priority = models.IntegerField("우선순위", default=0)

    class Meta:
        db_table = "post_image"
        verbose_name = "글 이미지"
        verbose_name_plural = "글 이미지 목록"


@receiver(pre_save, sender=PostImage)
def pre_save_post_image(sender, instance, **kwargs):
    post_id = instance.post_id

    if (
        post_id
        and sender.objects.exists(
            post_id=instance.post_id, priority=instance.priority
        ).exists()
    ):
        last_priority = (
            sender.objects.filter(post_id=post_id).order_by("priority").last()
        )
        if last_priority:
            instance.priority = last_priority.priority


class PostLike(BaseModel):
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "post_like"
        verbose_name = "글 좋아요"
        verbose_name_plural = "글 좋아요 목록"


class Comment(BaseModel):
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField("내용", max_length=100)

    class Meta:
        db_table = "post_comment"
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
