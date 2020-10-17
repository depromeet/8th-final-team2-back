from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from utils.permission import IsOwner
from . import serializers


class UserAPIView(GenericAPIView):
    permission_classes = [IsOwner]
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
