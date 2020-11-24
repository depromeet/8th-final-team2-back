from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    CommentViewSet,
)
from . import views

router = SimpleRouter()
router.register(r"", views.PostViewSet)

urlpatterns = [
    path("image/", views.PostImageAPIView.as_view()),
    path("like/", views.PostLikeAPIView.as_view()),
    path("comment/", CommentViewSet.as_view({"get": "list", "post": "create"})),
] + router.urls
