import uuid

from rest_framework.exceptions import ValidationError
from api.filters import TitleFilter
from api.permissions import IsUserAdminModeratorOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CommentSerializer, ReviewSerializer,
                             CategorySerializer, GenreSerializer,
                             TitleSerializer, SignupSerializer,
                             TokenSerializer, UserSerializer,
                             ProfileSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import viewsets, mixins, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from reviews.models import Review, Title, Category, Genre
from users.models import User


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [IsUserAdminModeratorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        title_queryset = title.reviews.all()
        return title_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsUserAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        review_queryset = review.comments.all()
        return review_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated, ])
def get_profile(request):
    if request.method == "PATCH":
        serializer = ProfileSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        username = serializer.initial_data.get("username")
        email = serializer.initial_data.get("email")

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            if instance.email != email:
                raise ValidationError("У данного пользователя другая почта!")
            serializer.is_valid(raise_exception=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_unusable_password()
        instance.save()
        email = serializer.validated_data["email"]

        code = uuid.uuid4()
        send_mail(
            "КОД ПОДТВЕРЖДЕНИЯ",
            f"Ваш код подтверждения!\n{code}",
            "from@example.com",
            [email],
            fail_silently=False,
        )
        instance.confirmation_code = code
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(TokenObtainPairView):

    serializer_class = TokenSerializer
