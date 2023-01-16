from api.views import (APIGetToken, APISignup, CategoriesViewSet,
                       CommentsViewSet, GenresViewSet, ReviewsViewSet,
                       TitlesViewSet, UsersViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)
router_v1.register('categories', CategoriesViewSet, basename='сategories')
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('genres', GenresViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
]
