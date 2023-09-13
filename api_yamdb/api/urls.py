from django.urls import include, path
from rest_framework import routers

from api.views import (
    APIGetToken,
    APISignUp,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

app_name = '%(app_label)s'

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='token'),
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
