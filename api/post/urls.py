from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostAPIView.as_view()),
    path("image/", views.PostImageAPIView.as_view()),
    path("like/", views.PostLikeAPIView.as_view()),
    path("<int:pk>/comment/", views.CommentAPIView.as_view()),
]
