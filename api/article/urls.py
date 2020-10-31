from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'', views.ArticleViewSet)

urlpatterns = [] + router.urls
