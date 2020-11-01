from django.db import models
from os import path
from uuid import uuid1

from utils.model import BaseModel
from apps.mission.models import Mission
from apps.user.models import User


class Article(BaseModel):
    title = models.CharField(max_length=20)
    content = models.TextField()
    mission = models.ForeignKey(
        Mission, related_name="mission", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        User, related_name="article_user", on_delete=models.DO_NOTHING
    )
    media_contents = models.ManyToManyField("MediaContent")
    like_users = models.ManyToManyField(
        User, through="ArticleLike", related_name="like_users",
    )


def upload_to(instance, filename):
    _, ext = path.splitext(filename)
    return f"upload/media/{uuid1()}{ext})"


class MediaContent(BaseModel):
    file = models.FileField(null=False, blank=False, upload_to=upload_to)

class ArticleLike(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        User, related_name="like_user", on_delete=models.DO_NOTHING
    )


class Comment(BaseModel):
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.DO_NOTHING
    )
    content = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, related_name="comment_user", on_delete=models.DO_NOTHING
    )

