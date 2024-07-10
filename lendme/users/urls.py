from django.urls import path


from users.auth.views import (
    RegisterView,
    LoginView,
    CustomTokenRefreshView,
    LogoutView
)
from users.views import (
    PasswordResetView,
    PasswordTokenCheck,
    SetNewPassword,
)

from users.auth.confirmation.views import (
    SmsCodeCreateView,
    SmsCodeVerificationView,
    SendEmailConfirmationTokenView,
    ConfirmEmailView,
)


urlpatterns = [
    # Регистрация/Авторизация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", CustomTokenRefreshView.as_view(), name="refresh_token"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Подтверждение телефона и почты
    path('send_sms/', SmsCodeCreateView.as_view(), name='send_sms'),
    path("confirm_phone/", SmsCodeVerificationView.as_view(), name="confirm_phone"),
    path("send_token_email/", SendEmailConfirmationTokenView.as_view(), name="send_token_email"),
    path("confirm_email/", ConfirmEmailView.as_view(), name="confirm_email"),

    # Сброс и создание нового пароля
    path("request-reset-password/", PasswordResetView.as_view(), name="request-reset-password"),
    path("password-reset/<uidb64>/<token>/", PasswordTokenCheck.as_view(), name="password-reset-confirm"),
    path("password-reset-complete/", SetNewPassword.as_view(), name="password-reset-complete"),
]
