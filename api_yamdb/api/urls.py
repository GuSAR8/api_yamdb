from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, ReviewViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet, UserViewSet, SignUpViewSet,
                    TokenView, get_profile)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register('users', UserViewSet, basename='users')
router.register("auth/signup", SignUpViewSet)

urlpatterns = [
    path("users/me/", get_profile, name="get_profile"),
    path('', include(router.urls)),
    path("auth/token/", TokenView.as_view(), name="token"),
]
