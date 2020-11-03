from django.contrib import admin

from .models import Article, Comment, MediaContent


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    pass