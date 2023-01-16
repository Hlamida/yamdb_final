from django_filters import rest_framework as filters


class TitlesFilter(filters.FilterSet):
    """Класс для фильтрации вывода произведений."""

    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains',
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='contains',
    )
    year = filters.NumberFilter(
        field_name='year',
        lookup_expr='contains',
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )
