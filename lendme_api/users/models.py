from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    """Модель Пользователя."""

    username = None
    name = models.CharField(
        "Имя пользователя",
        unique=False,
        max_length=70,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        "Почта",
        unique=True,
        max_length=254,
        blank=False,
        null=False,
    )
    phone_number = models.CharField(
        "Номер телефон",
        unique=True,
        max_length=10,
        blank=False,
        null=False,
        validators=[MinLengthValidator(10)],
    )
    profile_image = models.ImageField(
        "Аватар пользователя",
        upload_to="users/profile_image",
        blank=True,
        null=True,
    )
    password = models.CharField(
        "Пароль",
        max_length=128,
        blank=False,
        null=False,
    )
    confirmation_code = models.CharField(
        "Код подтверждения",
        max_length=5,
        blank=True
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_phone_verified = models.BooleanField(
        "Проверка телефона",
        default=False,
    )
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(
        "Проверка верификации",
        default=False,
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)

    def __str__(self):
        return f"Почта - {self.email}, телефон - {self.phone} пользователя."


class Favorite(models.Model):
    user = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Избранное",
    )
    product = ...


class Review(models.Model):
    client = models.ForeignKey(
        "CustomUser",
        verbose_name="Покупатель",
        related_name="client",
        on_delete=models.CASCADE,
    )
    seller = models.ForeignKey(
        "CustomUser",
        verbose_name="Продавец",
        related_name="seller",
        on_delete=models.CASCADE,
    )
    raiting = models.IntegerField(
        verbose_name="Рейтинг",
        default=0,
        validators=[MinLengthValidator(0), MinLengthValidator(5)],
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
