from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Article
from missions.serializers import MissionSerializer
from apps.user.models import User

class UserSerializer(ModelSerializer) :
    class Meta :
        model = User
        fields = [
            "nickname",
            "image",
        ]

class ArticleSerializer(ModelSerializer):
    mission = MissionSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
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


