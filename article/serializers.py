from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Article

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "mission",
            "created_at",
            "user",
        ]


