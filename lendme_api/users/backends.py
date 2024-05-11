from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger(__name__)

from .models import CustomUser


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

    def authenticate(self, request, phone_number, password) -> CustomUser | None:
        print(request)
        print(phone_number, password)
        try:
            user: CustomUser = CustomUser.objects.get(
                Q(email=phone_number) | Q(phone_number=phone_number)
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


class AdminAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(phone_number=username)
            if user.check_password(password) and user.is_staff:
                return user
        except CustomUser.DoesNotExist:
            return None
