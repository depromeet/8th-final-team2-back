from django.contrib import admin

from .models import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    pass