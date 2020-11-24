from rest_framework.serializers import ModelSerializer

from apps.mission.models import Mission


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "id",
            "name",
            "priority",
            "created_at",
        ]
