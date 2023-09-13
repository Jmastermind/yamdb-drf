from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnlyPermission


class CreateDeleteListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for model creation, deletion and list view."""

    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnlyPermission,)
