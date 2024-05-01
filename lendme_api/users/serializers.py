from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import NotFound

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор, который включает в себя атрибуты,
    необходимые для регистрации пользователя.
    """

    def validate_name(self, value)-> str:
        """Валидация на соответствие имени всем требованиям."""

        if not value.isalpha():
            raise ValidationError(_("Имя может содержать только буквы."))

        if len(value) < 2 or len(value) > 50:
            raise ValidationError(_("Имя должно содержать от 2 до 50 символов."))
        return value

    def validate_phone_number(self, value: str) -> str:
        """Валидации на соответствие номера телефона всем требованиям."""
        return value

    def validate_email(self, value: str) -> str:
        """Валидация на соответствие e-mail всем требованиям."""
        validate_email(value)
        return value

    def validate_password(self, value: str) -> str:
        """Валидация на соответствие пароля всем требованиям."""
        validate_password(value)
        return value

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "name",
            "email",
            "phone_number",
            "password",
            "is_superuser",
            "is_staff"
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}


class PhoneSmsSerializer(serializers.Serializer):
    """Сериализатор для номера телефона и смс кода."""

    phone_number = serializers.CharField(max_length=10)
    sms_code = serializers.IntegerField(required=False)

    @staticmethod
    def validate_phone_number(value):
        """Метод валидации номера телефона."""
        return value

    @staticmethod
    def validate_sms_code(value):
        """Метод валидации смс кода."""
        if len(str(value)) != 5:
            raise serializers.ValidationError(
                "Код должен состоять из 5 цифр"
            )
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор Token Obtain Pair Serializer

    Кастомный сериализатор добавляет дополнительные
    данные в токен, такие как email, phone_number и name
    """

    default_error_messages = {
        "no_active_account": _("Имя пользователя или пароль недействительны.")
    }

    @classmethod
    def get_token(cls, user):
        """Создание токена и добавление дополнительных данных."""
        token = super().get_token(user)

        # Добавление дополнительных данных
        if hasattr(user, "email"):
            token["email"] = user.email

        if hasattr(user, "phone_number"):
            token["phone_number"] = user.phone_number

        if hasattr(user, "name"):
            token["name"] = user.name

        return token


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор для сброса пароля."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def get_user(self, destination: str) -> CustomUser:

        try:
            user = CustomUser.objects.get(email=destination)
        except CustomUser.DoesNotExist:
            user = None
        return user

    def validate(self, attrs: dict) -> dict:
        """Проверяет, существует ли пользователь с
        предоставленной электронной почтой.
        """
        validator = EmailValidator()
        validator(attrs.get("email"))
        user = self.get_user(attrs.get("email"))

        if not user:
            raise NotFound(_("Пользователь с указанным адресом электронной почты не существует."))

        return attrs
