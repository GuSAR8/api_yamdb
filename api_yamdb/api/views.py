from api.serializers import GenreSerializer, CategorySerializer, TitleSerializer
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from reviews.models import Genre, Category


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        category = Category.kwargs.get('category_id')
        serializer.save(category=category)
        genre = Genre.kwargs.get('genre_id')
        serializer.save(genre=genre)
