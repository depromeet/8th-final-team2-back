from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'', views.ArticleViewSet)
router.register(r'<int:pk>', views.ArticleViewSet)
router.register(r'files', views.MediaContentViewSet)
urlpatterns = [] + router.urls
# from api.article.views import (
#     ArticleLikeViewSet,
#     ArticleViewSet,
#     CommentViewSet,
#     MediaContentViewSet,
# )
# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#     path("articles", ArticleViewSet.as_view({"get": "list", "post": "create"})),
#     path(
#         "articles/<int:pk>",
#         ArticleViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
#     ),
#     path("files", MediaContentViewSet.as_view({"get": "list", "post": "create"})),
#     path("like", ArticleLikeViewSet.as_view({"get": "list", "post": "create"})),
#     # path("comment", CommentViewSet.as_view({"get": "list", "post": "create"})),
#     path("comment", CommentViewSet.as_view({'get': 'list', "post": "create"})),
# ]
