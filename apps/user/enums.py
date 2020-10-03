from django.db import models


class Provider(models.TextChoices):
    DEFAULT = 'default', '기본'
    KAKAO = 'kakao', '카카오'
    GOOGLE = 'google', '구글'
