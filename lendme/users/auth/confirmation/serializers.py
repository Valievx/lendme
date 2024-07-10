from rest_framework import serializers
from django.core.exceptions import ValidationError

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


class SendEmailConfirmationTokenSerializer(serializers.Serializer):
    """Сериализатор для отправки токена подтверждения на почту."""
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        user = self.context["request"].user
        if user.email != value:
            raise ValidationError("Указанный адрес электронной почты не соответствует.")
        return value
