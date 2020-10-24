from os import name
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(("api.urls", "api"), namespace="api")),
    path("api/v1/", include("missions.urls")),
    path("api/v1/", include("article.urls")),
]
