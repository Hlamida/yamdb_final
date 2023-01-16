from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsAdminUserOrReadOnly


class CategoryGenreMixin(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                         GenericViewSet):
    '''Миксин для вьюсетов категорий и жанров'''

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
