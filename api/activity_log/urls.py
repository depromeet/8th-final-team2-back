from django.urls import path

from .views import (
    ActivityLogViewSet
)
from . import views

urlpatterns = [
    path("", views.ActivityLogViewSet.as_view({'get':'list'})),
]
