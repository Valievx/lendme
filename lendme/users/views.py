from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer

from django.utils import timezone
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.conf import settings
from django.middleware.csrf import get_token

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

from .core.ip_service import get_client_ip, get_location_by_ip
from users.models import CustomUser, AuthTransaction, EmailConfirmationToken

from .core.code_generation import send_reset_password

from users.serializers import (
    UserSerializer,
    PhoneSmsSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
    SendEmailConfirmationTokenSerializer,
    SetNewPasswordSerializer
)

from drf_spectacular.utils import (
    # OpenApiParameter,
    extend_schema,
    extend_schema_view,
)


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Авторизация пользователя",
    ),
)
class LoginView(APIView):
    """
    Авторизация

    Используется для входа в систему.
    Требуемые данные: phone_number или email и password.
    """

    # renderer_classes = (JSONRenderer,)
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

        # if not user.is_phone_verified:
        #     return JsonResponse(
        #         {"error": _("Номер телефона не подтвержден.")},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

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
            city=city,
        ).save()

        response = Response(
            {
                "refresh_token": str(refresh_token),
                "token": str(token),
                "session": user.get_session_auth_hash(),
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT["TOKEN_COOKIE_NAME"],
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        csrf_token = get_token(request)
        response.set_cookie(
            key="csrftoken", value=csrf_token, secure=True, samesite="Strict"
        )

        return response


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Создание пользователя",
    ),
)
class RegisterView(CreateAPIView):
    """
    Регистрация

    Регистрация нового пользователя.
    Требуемые данные: name, email, password, phone_number.
    """

    # renderer_classes = (JSONRenderer,)
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


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Обновление токена",
    ),
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

        response = Response({"token": str(token)}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT["TOKEN_COOKIE_NAME"],
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        csrf_token = get_token(request)
        response.set_cookie(
            key="csrftoken", value=csrf_token, secure=True, samesite="Strict"
        )

        return response


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Смена пароля",
    ),
)
class PasswordResetView(APIView):
    """Сброс пароля

    Отправка на email инструкции для сброса пароля.
    Требуемые данные: email.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        """Метод сброса пароля"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"message": "Пользователь с таким адресом электронной почты не существует"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                "password-reset-confirm",
                kwargs={"uidb64": uidb64, "token": token}
            )
            absurl = "http://" + current_site + relative_link
            send_reset_password(absurl, email)
            return Response(
                {"message": "Мы отправили вам ссылку для сброса пароля"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Пользователи"],
    methods=["GET"],
)
@extend_schema_view(
    get=extend_schema(
        summary="Проверка действительности токена",
    ),
)
class PasswordTokenCheck(APIView):
    """
    Проверка действительности токена, который
    используется для сброса пароля пользователя

    Требуемые данные: token, uidb64.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, uidb64, token):
        """Метод проверяет действительность токена сброса пароля."""
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"message": "Токен недействителен, запросите новый."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(
                {"success": True,
                 "message": "Токен действителен",
                 "uidb64": uidb64,
                 "token": token
                 },
                status=status.HTTP_200_OK
            )

        except DjangoUnicodeDecodeError as e:
            return Response(
                {"message": f"Токен недействителен, запросите новый. {e}"},
                status=status.HTTP_401_UNAUTHORIZED
            )


@extend_schema(
    tags=["Пользователи"],
    methods=["PATCH"],
)
@extend_schema_view(
    patch=extend_schema(
        summary="Установка нового пароля",
    ),
)
class SetNewPassword(APIView):
    """
    Установка нового пароля пользователя
    после успешного сброса пароля.

    Требуемые данные: password, token, uidb64.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """Метод для обновления пароля."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(
                {"success": True,
                 "message": "Пароль успешно обновлен"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"success": False,
                 "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Выход из системы",
    ),
)
class LogoutView(APIView):
    """
    Выход из системы

    Используется для выхода из системы.
    """

    def post(self, request):
        """Метод для выхода из системы."""
        try:
            jwt_auth = JWTAuthentication()
            user, _ = jwt_auth.authenticate(request)
            if user:
                Token.objects.filter(user=user).delete()
                return Response(
                    {"message": "Вы успешно вышли из системы."},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"message": f"Не удалось выйти из системы.{e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
