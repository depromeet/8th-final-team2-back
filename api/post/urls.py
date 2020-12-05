from django.urls import path

from .views import (
    CommentViewSet,
)
from . import views

urlpatterns = [
    path("", views.PostAPIView.as_view()),
    path("image/", views.PostImageAPIView.as_view()),
    path("like/", views.PostLikeAPIView.as_view()),
    path("comment/", CommentViewSet.as_view({"get": "list", "post": "create"})),
]
