from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from users.core.code_generation import (
    generate_sms_code, send_sms_code,
    send_confirmation_email, send_reset_password
)
from users.serializers import (
    PhoneSmsSerializer,
    SendEmailConfirmationTokenSerializer,
)
from users.models import CustomUser, EmailConfirmationToken


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
    get=extend_schema(
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
