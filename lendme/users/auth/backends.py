from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger(__name__)

from users.models import CustomUser


class AuthBackend(ModelBackend):
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def get_user(self, user_id) -> CustomUser | None:
        print(user_id)
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def authenticate(self, request, password, phone_number=None, username=None) -> CustomUser | None:
        print(request)
        print(phone_number, password, username)
        try:
            user: CustomUser = CustomUser.objects.get(
                Q(username=username) | Q(email=username) | Q(phone_number=username)
            )
            print(user.check_password(password))

        except CustomUser.DoesNotExist:
            return None

        if user.email == phone_number and not user.is_email_verified:
            raise ValidationError(_("Email не подтвержден."))

        if user.phone_number == phone_number and not user.is_phone_verified:
            raise ValidationError(_("Телефон не подтвержден."))

        if user.check_password(password):
            print("1")
            return user

        else:
            return None
