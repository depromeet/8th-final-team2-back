from django_filters.rest_framework.filterset import FilterSet

from apps.post.models import Post


class PostFilterSet(FilterSet):
    class Meta:
        model = Post
        fields = ["mission"]
