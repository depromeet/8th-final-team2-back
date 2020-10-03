from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .enums import Provider
from .managers import UserManager
from .images import path_user_image


class User(AbstractBaseUser):
    username = models.CharField("아이디", max_length=100, unique=True)
    provider = models.CharField(
        "플랫폼", max_length=20, choices=Provider.choices, default=Provider.DEFAULT)
    nickname = models.CharField("닉네임", max_length=100, null=True, blank=True)
    image = models.ImageField(
        "이미지", upload_to=path_user_image, null=True, blank=True)

    is_active = models.BooleanField('활성여부', default=True)
    date_join = models.DateTimeField("가입일", auto_now_add=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        verbose_name_plural = "유저 목록"
