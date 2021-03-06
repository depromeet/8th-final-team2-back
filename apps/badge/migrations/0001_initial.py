# Generated by Django 3.1.3 on 2020-12-01 12:58

import apps.badge.images
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='아이콘명')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.badge.images.path_profile_icon_image, verbose_name='이미지')),
                ('active_image', models.ImageField(blank=True, null=True, upload_to=apps.badge.images.path_profile_icon_image, verbose_name='활성이미지')),
                ('priority', models.PositiveIntegerField(default=0, verbose_name='우선순위')),
            ],
            options={
                'verbose_name': '프로필 아이콘',
                'verbose_name_plural': '프로필 아이콘 목록',
                'db_table': 'profile_icon',
            },
        ),
        migrations.CreateModel(
            name='UserProfileIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquired_date', models.DateTimeField(auto_now_add=True, verbose_name='획득날짜')),
                ('icon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badge.profileicon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '사용자 프로필 아이콘',
                'verbose_name_plural': '사용자 프로필 아이콘 목록',
                'db_table': 'profile_icon_user',
            },
        ),
    ]
