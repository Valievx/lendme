import re

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from rest_framework import serializers

from users.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор, который включает в себя атрибуты,
    необходимые для регистрации пользователя.
    """

    def validate_name(self, value)-> str:
        """Валидация на соответствие требованиям для name."""
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

    phone_number = serializers.CharField(max_length=12)
    sms_code = serializers.IntegerField(required=False)

    @staticmethod
    def validate_phone_number(value):
        """Метод валидации номера телефона."""
        pattern = r'\+7\d{10}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Номер телефона должен начинаться с +7 и иметь 11 цифр"
            )
        return value

    @staticmethod
    def validate_sms_code(value):
        """Метод валидации смс кода."""
        if len(str(value)) != 5:
            raise serializers.ValidationError(
                "Код должен состоять из 5 цифр"
            )
        return value
