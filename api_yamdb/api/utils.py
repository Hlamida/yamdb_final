from api.permissions import IsAdminUserOrReadOnly
from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class CategoryGenreMixin(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                         GenericViewSet):
    '''Миксин для вьюсетов категорий и жанров'''

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
