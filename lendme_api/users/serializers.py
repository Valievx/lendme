from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
            "password"
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}


class PhoneSmsSerializer(serializers.Serializer):
    """Сериализатор для номера телефона и смс кода."""

    phone_number = serializers.CharField(max_length=12)
    sms_code = serializers.CharField(required=False)


    def validate_phone_number(self, value: str) -> str:
        """Метод валидации номера телефона."""
        return value


    def validate_sms_code(self, value: str) -> str:
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
            token["phone_number"] = str(user.phone_number)

        if hasattr(user, "name"):
            token["name"] = user.name

        return token


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор для сброса пароля."""

    email = serializers.EmailField(required=True)

    def validate_email(self, value: str) -> str:
        """
        Проверяет, существует ли пользователь
        с предоставленной электронной почтой.
        """
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким адресом электронной почты не существует"
            )
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    """Сериализатор для создания нового пароля."""

    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Недействительная ссылка для сброса пароля")

            user.set_password(password)
            user.save()

            return user

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        except Exception:
            raise serializers.ValidationError("Недействительная ссылка для сброса пароля")


class SendEmailConfirmationTokenSerializer(serializers.Serializer):
    """Сериализатор для отправки токена подтверждения на почту."""
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        user = self.context["request"].user
        if user.email != value:
            raise ValidationError("Указанный адрес электронной почты не соответствует.")
        return value
