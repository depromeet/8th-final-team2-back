from django.db import models

from utils.model import BaseModel


class Mission(BaseModel):
    name = models.CharField("제목", max_length=150)
    priority = models.IntegerField("우선순위", default=0)

    class Meta:
        db_table = "mission"
        verbose_name = "미션"
        verbose_name_plural = "미션 목록"

    def __str__(self):
        return self.name