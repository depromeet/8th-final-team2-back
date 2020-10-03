from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Mission

class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "id",
            "title",
            "description",
            "level",
        ]