from article.views import (
    ArticleViewSet,
)
from django.urls import path

from . import views

urlpatterns = [
    path("articles", ArticleViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "articles/<int:pk>",
        ArticleViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
    ),
]
