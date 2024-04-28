from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from rest_framework import serializers

from users.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор, который включает в себя атрибуты,
    необходимые для регистрации пользователя.
    """

    def validate_name(self, value):
        """Валидация на соответствие требованиям для name."""
        return value

    def validate_phone(self, value: str) -> str:
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
            "phone",
            "password",
            "is_superuser",
            "is_staff"
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}
