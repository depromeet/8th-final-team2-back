from django.contrib import admin

from .models import ProfileIcon, UserProfileIcon


@admin.register(ProfileIcon)
class ProfileIconAdmin(admin.ModelAdmin):
    list_display = ["name", "priority"]


@admin.register(UserProfileIcon)
class UserProfileIconAdmin(admin.ModelAdmin):
    pass