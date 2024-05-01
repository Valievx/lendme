from django.http import HttpResponse

from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import get_object_or_404

from users.serializers import UserSerializer, PhoneSmsSerializer
from users.models import CustomUser
from users.services import generate_sms_code, send_sms_code


def login_view(request):
    return HttpResponse("Login view placeholder")

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
            access_token = str(AccessToken.for_user(user))
            return Response(
                {'message': 'Номер телефона успешно подтвержден',
                'access_token': access_token},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Неправильный смс код'},
                status=status.HTTP_400_BAD_REQUEST
            )

def profile_view(request):
    return HttpResponse("Profile view placeholder")

def profile_update_view(request):
    return HttpResponse("Profile update view placeholder")

def reset_user_password_view(request):
    return HttpResponse("Reset user password view placeholder")

def refresh_token_view(request):
    return HttpResponse("Refresh token view placeholder")