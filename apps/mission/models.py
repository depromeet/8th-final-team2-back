from django.db import models

from utils.model import BaseModel


class Mission(BaseModel):
    title = models.CharField(max_length=20)
    description = models.TextField()
    level = models.IntegerField()
