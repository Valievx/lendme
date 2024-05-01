from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from users.utils import get_client_ip, get_location_by_ip
from users.models import CustomUser, AuthTransaction
from users.services import generate_sms_code, send_sms_code
from users.serializers import (UserSerializer, PhoneSmsSerializer,
                               CustomTokenObtainPairSerializer,
                               PasswordResetSerializer)


class LoginView(APIView):
    """
    Авторизация

    Используется для входа в систему.
    Требуемые данные: phone_number или email и password.
    """

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        """
        Метод обрабатывает POST запрос для входа
        через phone_number or email/password.
        """
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.user

        if not user.is_phone_verified:
            return JsonResponse(
                {'error': _('Номер телефона не подтвержден.')},
                status=status.HTTP_403_FORBIDDEN
            )

        token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        ip_address = get_client_ip(request)
        geo_location = get_location_by_ip(ip_address)
        city = geo_location.get("city") if geo_location else None

        AuthTransaction(
            created_by=user,
            token=str(token),
            refresh_token=str(refresh_token),
            ip_address=get_client_ip(self.request),
            session=user.get_session_auth_hash(),
            expires_at=timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME,
            city=city
        ).save()

        response  = {
            "refresh_token": str(refresh_token),
            "token": str(token),
            "session": user.get_session_auth_hash(),
            "city": city
        }
        return Response(response , status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    """
    Регистрация

    Регистрация нового пользователя.
    Требуемые данные: name, email, password, phone_number.
    """

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


    def perform_create(self, serializer):
        """Переопределение perform_create для создания пользователя"""
        data = {
            "name": serializer.validated_data["name"],
            "phone_number": serializer.validated_data["phone_number"],
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
        }
        return CustomUser.objects.create_user(**data)


class SmsCodeCreateView(APIView):
    """
    Создание SMS кода
    Требуемые данные: phone_number.
    """

    permission_classes = (AllowAny,)


    def post(self, request):
        """Метод обрабатывает POST запрос для отправки смс кода."""
        phone_number = request.data.get('phone_number')
        serializer = PhoneSmsSerializer(data={'phone_number': phone_number})
        if serializer.is_valid():
            try:
                sms_code = generate_sms_code()
                send_sms_code(phone_number, sms_code)

                user = CustomUser.objects.get(phone_number=phone_number)
                user.confirmation_code = sms_code
                user.save()

                return Response(
                    {'message': 'Смс код отправлен успешно',
                     'Никому не говорите код LendMe': sms_code},
                    status=status.HTTP_200_OK
                )
            except CustomUser.DoesNotExist:
                return Response(
                    {'message': 'Пользователь с указанным номером телефона не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'message': f'Ошибка отправки смс кода: {e}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=400)


class SmsCodeVerificationView(APIView):
    """
    Проверка SMS кода

    Проверка смс кода на подтверждение номера телефона.
    Требуемые данные: phone_number, sms_code.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод обрабатывает POST запрос для проверки смс кода."""
        phone_number = request.data.get('phone_number')
        sms_code = request.data.get('sms_code')
        user = get_object_or_404(CustomUser, phone_number=phone_number)

        if sms_code == user.confirmation_code:
            user.is_phone_verified = True
            user.save()
            return Response(
                {'message': 'Номер телефона успешно подтвержден'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Неправильный смс код'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenRefreshView(TokenRefreshView):
    """
    Подкласс TokenRefreshView для обновления модели
    AuthTransaction при обновлении токена доступа
    """

    def post(self, request):
        """
        Запрос на создание access token,
        используя refresh token.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        token = serializer.validated_data.get("access")

        auth_transaction = AuthTransaction.objects.get(
            refresh_token=request.data["refresh"]
        )
        auth_transaction.token = token
        auth_transaction.expires_at = (
            timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME
        )
        auth_transaction.save(update_fields=["token", "expires_at"])

        return Response({"token": str(token)}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    """Сброс пароля"""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод сброса пароля"""
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.get(email=serializer.validated_data["email"])

        if serializer.validated_data["email"]:
            user.set_password(serializer.validated_data["password"])
            user.save()
            return JsonResponse(
                {"message": "Пароль успешно обновлен."},
                status=status.HTTP_202_ACCEPTED,
            )
