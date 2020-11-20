from django.urls import path

from . import views

urlpatterns = [
    path("social/", views.SocialAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("profile/", views.ProfileAPIView.as_view()),
]
