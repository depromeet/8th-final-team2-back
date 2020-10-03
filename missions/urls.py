from missions.views import (
    MissionViewSet,
)
from django.urls import path

from . import views

urlpatterns = [
    path("missions", MissionViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "missions/<int:pk>",
        MissionViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
    ),
]
