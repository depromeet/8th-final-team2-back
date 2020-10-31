from rest_framework.serializers import ModelSerializer

from apps.mission.models import Mission


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "id",
            "title",
            "description",
            "level",
            "created_at",
        ]
