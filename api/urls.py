from os import name
from django.urls import path, include

urlpatterns = [
    path("user/", include(("api.user.urls", "user"), namespace="user")),
]
