from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from utils.permission import IsOwnerOrReadOnly


class UserAPIView(GenericAPIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return Response()
