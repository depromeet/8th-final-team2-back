from django.db import models
from commons.models import BaseModel
from missions.models import Mission

class Article(BaseModel) : 
    title = models.CharField(max_length=20)
    content = models.TextField() 
    mission = models.ForeignKey(
        Mission, related_name="mission", on_delete = models.DO_NOTHING)


class ArticleLike(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING)


class Comment(BaseModel):
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.DO_NOTHING
    )
    content = models.CharField(max_length=100)
