from django.http import HttpResponse

from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

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

    @staticmethod
    def post(request):
        """Метод обрабатывает POST запрос для отправки смс кода."""
        phone_number = request.data.get('phone_number')
        serializer = PhoneSmsSerializer(data={'phone_number': phone_number})
        if serializer.is_valid():
            try:
                sms_code = generate_sms_code()
                send_sms_code(phone_number, sms_code)
                return Response(
                    {'message': 'Смс код отправлен успешно',
                     'Код авторизации': {sms_code}},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'message': f'Ошибка отправки смс кода: {e}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=400)


def confirm_phone_view(request):
    return HttpResponse("Confirm phone view placeholder")

def profile_view(request):
    return HttpResponse("Profile view placeholder")

def profile_update_view(request):
    return HttpResponse("Profile update view placeholder")

def reset_user_password_view(request):
    return HttpResponse("Reset user password view placeholder")

def refresh_token_view(request):
    return HttpResponse("Refresh token view placeholder")