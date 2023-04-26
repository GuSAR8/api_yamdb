import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    ]

    username = models.CharField(
        'Логин',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=True,
        null=False
    )

    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
        blank=True,
        null=False
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Статус',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
        blank=True
    )
    confirmation_code = models.UUIDField(
        'Код потдверждения',
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
