from os import name
from django.urls import path, include

urlpatterns = [
    path("user/", include(("api.user.urls", "user"), namespace="user")),
    path("mission/", include(("api.mission.urls", "mission"), namespace="mission")),
    path("article/", include(("api.article.urls", "article"), namespace="article")),
]
