from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, ReviewViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet, UserViewSet, signup, get_token)

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
<<<<<<< HEAD
    basename='comment')
router.register(r'users', UserViewSet, basename='user')
=======
    basename='comments')
router.register('users', UserViewSet, basename='users')
>>>>>>> 6053249fd1f149fed5950604410c7588be4a9a8c

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='singup'),
    path('v1/auth/token/', get_token, name='token'),
]
