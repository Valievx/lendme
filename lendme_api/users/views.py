from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse
from django.conf import settings
from django.middleware.csrf import get_token
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

from users.utils import get_client_ip, get_location_by_ip
from users.models import CustomUser, AuthTransaction, EmailConfirmationToken

from users.services import (
    generate_sms_code, send_sms_code,
    send_confirmation_email, send_reset_password
)
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


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Отправка смс кода",
    ),
)
class SmsCodeCreateView(APIView):
    """
    Создание SMS кода
    Требуемые данные: phone_number.
    """

    permission_classes = (AllowAny,)
    serializer_class = PhoneSmsSerializer

    def post(self, request):
        """Метод обрабатывает POST запрос для отправки смс кода."""
        phone_number = request.data.get("phone_number")
        serializer = PhoneSmsSerializer(data={"phone_number": phone_number})
        if serializer.is_valid():
            try:
                sms_code = generate_sms_code()
                send_sms_code(phone_number, sms_code)

                # Сохраняем код подтверждения в Redis
                cache.set(phone_number, sms_code, timeout=None)

                return Response(
                    {
                        "message": "Смс код отправлен успешно",
                        "Никому не говорите код LendMe": sms_code,
                    },
                    status=status.HTTP_200_OK,
                )
            except CustomUser.DoesNotExist:
                return Response(
                    {"message": "Пользователь с указанным номером телефона не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                return Response(
                    {"message": f"Ошибка отправки смс кода: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=400)


@extend_schema(
    tags=["Пользователи"],
    methods=["POST"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Верификация Пользователя",
    ),
)
class SmsCodeVerificationView(APIView):
    """
    Проверка SMS кода

    Проверка смс кода на подтверждение номера телефона.
    Требуемые данные: phone_number, sms_code.
    """

    permission_classes = (AllowAny,)
    serializer_class = PhoneSmsSerializer

    def post(self, request):
        """Метод обрабатывает POST запрос для проверки смс кода."""
        phone_number = request.data.get("phone_number")
        sms_code = request.data.get("sms_code")
        user = get_object_or_404(CustomUser, phone_number=phone_number)

        # Получаем SMS-код из Redis
        stored_sms_code = cache.get(phone_number)

        # Преобразуем stored_sms_code в строку для сравнения
        stored_sms_code_str = str(stored_sms_code) if stored_sms_code is not None else None

        if stored_sms_code_str and isinstance(sms_code, str):
            if sms_code == stored_sms_code_str:
                user.is_phone_verified = True
                user.save()
                return Response(
                    {"message": "Номер телефона успешно подтвержден"},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "Неправильный смс код"},
            status=status.HTTP_400_BAD_REQUEST
        )


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
    post=extend_schema(
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
    post=extend_schema(
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
        summary="Подтверждение Email",
    ),
)
class SendEmailConfirmationTokenView(APIView):
    """
    Подтверждение Email

    Отправка на email токена для подтверждения почты.
    Требуемые данные: email.
    """

    permission_classes = (AllowAny,)
    serializer_class = SendEmailConfirmationTokenSerializer

    def post(self, request):
        """
        Метод обрабатывает POST запрос
        на отправку токена по почту.
        """
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            token = PasswordResetTokenGenerator().make_token(user)
            email_confirmation_token = EmailConfirmationToken.objects.create(
                user=user,
                token=token
            )
            uidb64 = urlsafe_base64_encode(force_str(user.pk).encode())
            token_str = email_confirmation_token.token

            send_confirmation_email(user.email, uidb64, token_str)
            return Response(
                {"message": "Токен успешно отправлен."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Пользователи"],
    methods=["GET"],
)
@extend_schema_view(
    post=extend_schema(
        summary="Подтверждения токена по почте",
    ),
)
class ConfirmEmailView(APIView):
    """
    Метод обрабатывает GET запрос
    подтверждения токена по почте.

    Требуемые данные: uidb64 и token.
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Метод обрабатывает GET запрос
        подтверждения токена по почте.

        Требуемые данные: uidb64 и token.
        """

        uidb64 = request.GET.get("uidb64")
        token = request.GET.get("token")

        try:
            print(uidb64)
            id = force_str(urlsafe_base64_decode(uidb64), encoding='latin-1')
            print(id)
            user = CustomUser.objects.get(id=id)
            print(user)
            token_obj = EmailConfirmationToken.objects.get(token=token, user=user)
            print(token_obj)

            if token_obj.is_valid():
                user.is_email_verified = True
                user.save()
                token_obj.delete()
                return JsonResponse(
                    {"message": "Email успешно подтвержден"},
                    status=status.HTTP_200_OK
                )
            else:
                return JsonResponse(
                    {"message": "Недействительный токен или истек срок действия"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return JsonResponse(
                {"message": f"Недействительный токен или идентификатор пользователя, {e}"},
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
