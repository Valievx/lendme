from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from ..services import send_confirmation_email
from ..models import EmailConfirmationToken


@receiver(post_save, sender=get_user_model())
def post_register(sender, instance, created, **kwargs):
    """Создает токен подтверждения почты для нового пользователя и отправляет сообщение."""
    if created:
        # Создаем токен подтверждения почты для нового пользователя
        token = PasswordResetTokenGenerator().make_token(instance)
        EmailConfirmationToken.objects.create(
            user=instance,
            token=token
        )
        # Отправляем сообщение пользователю
        uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))
        send_confirmation_email(instance.email, uidb64, token)
