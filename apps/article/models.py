from django.db import models

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
