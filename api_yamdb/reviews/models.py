from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Genre(models.Model):
    """Модель Жанров."""

    name = models.CharField('Жанры', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель Категорий."""

    name = models.CharField('Категорий', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведения."""
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField(verbose_name='Год издания')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='title',
        verbose_name='Жанр произведения',
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Описание произведения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['id']


class Review(models.Model):
    """Модель Отзывов и Рейтинга."""
    text = models.TextField(
        help_text='Введите текст отзыва',
        verbose_name='Текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10'),
        ],
        verbose_name='Оценка произведения',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение с отзывом',
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель Комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв с комментарием',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
