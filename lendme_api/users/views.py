from django.http import HttpResponse

from rest_framework.generics import CreateAPIView

from users.serializers import UserSerializer
from users.models import CustomUser
from users.services import generate_sms_code, send_sms_code


def login_view(request):
    return HttpResponse("Login view placeholder")

class RegisterView(CreateAPIView):
    """
    Регистрация

    Регистрация нового пользователя.
    Требуемые данные: name, email, password, phone, confirmation_code.
    """

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Переопределение perform_create для создания пользователя"""
        data = {
            "name": serializer.validated_data["name"],
            "phone": serializer.validated_data["phone"],
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
        }
        return CustomUser.objects.create_user(**data)


def send_sms_view(request):
    return HttpResponse("Send SMS view placeholder")

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