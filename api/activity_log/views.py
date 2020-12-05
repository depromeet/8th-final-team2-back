from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.activity_log.models import ActivityLog

from . import serializers

class ActivityLogViewSet(ModelViewSet) :
    queryset = ActivityLog.objects.all()
    serializer_class = serializers.ActivityLogSerializer
