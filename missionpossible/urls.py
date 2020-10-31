from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MissionPossible API",
        default_version='v1',
        description="디프만 파이널 프로젝트",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(("api.urls", "api"), namespace="api")),
    path("api/v1/", include("missions.urls")),
    path("api/v1/", include("article.urls")),
    path("swagger/", schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
]
