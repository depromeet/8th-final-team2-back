from rest_framework.serializers import ModelSerializer

from apps.activity_log.models import ActivityLog


class ActivityLogSerializer(ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "user",
            "content",
            "exp",
            "created_at",
        ]
