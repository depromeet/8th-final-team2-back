from rest_framework.serializers import ModelSerializer

from api.mission.serializers import MissionSerializer
from apps.article.models import Article
from apps.user.models import User


class UserSerializer(ModelSerializer):
    class Meta:
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
