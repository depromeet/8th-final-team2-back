from rest_framework import viewsets

from apps.mission.models import Mission
from . import serializers


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = serializers.MissionSerializer
