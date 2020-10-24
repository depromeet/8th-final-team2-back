from django.db import models
from .images import path_profile_icon_image


class ProfileIcon(models.Model):
    name = models.CharField('아이콘명', max_length=150)
    image = models.ImageField(
        '이미지', upload_to=path_profile_icon_image, null=True, blank=True)
    priority = models.PositiveIntegerField('우선순위', default=0)

    class Meta:
        db_table = 'profile_icon'


class UserProfileIcon(models.Model):
    icon = models.ForeignKey('badge.ProfileIcon', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    acquired_date = models.DateTimeField('획득날짜', null=True, blank=True)

    class Meta:
        db_table = 'profile_icon_user'
