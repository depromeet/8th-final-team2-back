from django.urls import path

from . import views

urlpatterns = [
    path('social/', views.SocialAPIView.as_view()),
]
