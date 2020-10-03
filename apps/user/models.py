from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .enums import Provider
from .managers import UserManager
from .images import path_user_image


class User(AbstractBaseUser):
    username = models.CharField("아이디", max_length=100, unique=True)
    provider = models.CharField(
        "플랫폼", max_length=20, choices=Provider.choices, default=Provider.DEFAULT)
    uid = models.CharField("UID", max_length=255, null=True, blank=True)
    nickname = models.CharField("닉네임", max_length=100, null=True, blank=True)
    image = models.ImageField(
        "이미지", upload_to=path_user_image, null=True, blank=True)

    is_active = models.BooleanField('활성여부', default=True)
    is_admin = models.BooleanField("관리자여부", default=False)
    date_join = models.DateTimeField("가입일", auto_now_add=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        verbose_name_plural = "유저 목록"

    @property
    def is_staff(self):
        return self.is_active and self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return self.is_active
