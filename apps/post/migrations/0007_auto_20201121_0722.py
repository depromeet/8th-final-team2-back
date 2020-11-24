# Generated by Django 3.1.3 on 2020-11-20 22:22

import apps.post.images
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mission", "0002_auto_20201121_0642"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0006_auto_20201121_0114"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                ("content", models.TextField(blank=True, null=True, verbose_name="내용")),
            ],
            options={
                "verbose_name": "글",
                "verbose_name_plural": "글 목록",
                "db_table": "post",
            },
        ),
        migrations.CreateModel(
            name="PostImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                (
                    "image",
                    models.ImageField(
                        upload_to=apps.post.images.path_post_image,
                        verbose_name="이미지",
                    ),
                ),
                ("priority", models.IntegerField(default=0, verbose_name="우선순위")),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="post.post"
                    ),
                ),
            ],
            options={
                "verbose_name": "글 이미지",
                "verbose_name_plural": "글 이미지 목록",
                "db_table": "post_image",
            },
        ),
        migrations.CreateModel(
            name="PostLike",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="post.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "글 좋아요",
                "verbose_name_plural": "글 좋아요 목록",
                "db_table": "post_like",
            },
        ),
        migrations.RemoveField(
            model_name="post",
            name="like_users",
        ),
        migrations.RemoveField(
            model_name="post",
            name="media_contents",
        ),
        migrations.RemoveField(
            model_name="post",
            name="mission",
        ),
        migrations.RemoveField(
            model_name="post",
            name="user",
        ),
        migrations.DeleteModel(
            name="PostLike",
        ),
        migrations.DeleteModel(
            name="MediaContent",
        ),
        migrations.AddField(
            model_name="post",
            name="like",
            field=models.ManyToManyField(
                related_name="like_users",
                through="post.PostLike",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="mission",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mission.mission"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="post.post"
            ),
        ),
        migrations.DeleteModel(
            name="Post",
        ),
    ]
