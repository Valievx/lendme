from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    """Модель Пользователя."""
    # Когда перейдем на PostgreSQL установить id
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = None
    name = models.CharField(
        "Имя пользователя",
        unique=False,
        max_length=50,
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
    phone_number = PhoneNumberField(
        # Номер телефона начинается с +7
        "Номер телефон",
        region='RU',
        unique=True,
        max_length=12,
        blank=False,
        null=False,
        validators=[MinLengthValidator(12)],
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
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_phone_verified = models.BooleanField(
        "Проверка телефона",
        default=False,
    )
    is_email_verified = models.BooleanField(
        "Проверка email",
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
        return f"Почта - {self.email}, телефон - {self.phone_number} пользователя."


class AuthTransaction(models.Model):
    """Модель мета данных Аутентификации."""
    ip_address = models.GenericIPAddressField(
        blank=False,
        null=False
    )
    city = models.CharField(
        "Город",
        max_length=100,
        blank=True,
        null=True
    )
    token = models.TextField(
        "JWT Access Token"
    )
    session = models.TextField(
        "Session"
    )
    refresh_token = models.TextField(
        "JWT Refresh Token",
        blank=True,
    )
    expires_at = models.DateTimeField(
        "Дата окончания",
        blank=True,
        null=True
    )
    create_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        "Дата обновления",
        auto_now=True
    )
    created_by = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return str(self.created_by.name) + " | " + str(self.created_by.username)

    class Meta:
        verbose_name = "Транзакция аутентификации"
        verbose_name_plural = "Транзакции аутентификаций"


class EmailConfirmationToken(models.Model):
    """Модель токена подтверждения Email почты."""
    # Когда перейдем на PostgreSQL установить id
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(
        max_length=64,
        default=PasswordResetTokenGenerator().make_token
    )

    def is_valid(self):
        """Проверяет, действителен ли токен."""
        return self.created_at >= timezone.now() - timezone.timedelta(minutes=20)


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
