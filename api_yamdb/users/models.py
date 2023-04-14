from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):  # Создаем свой класс пользователя
    #  Прописываем возможные роли
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
    )

    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=True,
    )

    bio = models.TextField(
        verbose_name='Биография',
        null=True,
    )

    role = models.CharField(
        verbose_name='Статус',
        max_length=9,
        choices=ROLES,
        default='USER'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("id",)

    def __str__(self):
        return self.username
