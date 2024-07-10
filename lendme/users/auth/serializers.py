from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор Token Obtain Pair Serializer

    Кастомный сериализатор добавляет дополнительные
    данные в токен, такие как email, phone_number и name
    """

    default_error_messages = {
        "no_active_account": _(
            "Имя пользователя или пароль недействительны."
        )
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
