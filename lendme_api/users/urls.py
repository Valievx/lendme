from django.urls import path


from users.views import (
    LoginView,
    RegisterView,
    SmsCodeCreateView,
    SmsCodeVerificationView,
    PasswordResetView,
    PasswordTokenCheck,
    CustomTokenRefreshView,
    SendEmailConfirmationTokenView,
    SetNewPassword,
    ConfirmEmailView
)


urlpatterns = [
    # api/user/register/
    path("register/", RegisterView.as_view(), name="register"),
    # api/user/send_sms/
    path('send_sms/', SmsCodeCreateView.as_view(), name='send_sms'),
    # api/user/confirm_phone/
    path("confirm_phone/", SmsCodeVerificationView.as_view(), name="confirm_phone"),
    # api/user/send_token_email/
    path("send_token_email/", SendEmailConfirmationTokenView.as_view(), name="send_token_email"),
    # api/user/confirm_email/
    path("confirm_email/", ConfirmEmailView.as_view(), name="confirm_email"),
    # api/user/login/
    path("login/", LoginView.as_view(), name="login"),
    # api/user/request-reset-password/
    path("request-reset-password/", PasswordResetView.as_view(), name="request-reset-password"),
    # api/user/password-reset/<uidb64>/<token>/
    path("password-reset/<uidb64>/<token>/", PasswordTokenCheck.as_view(), name="password-reset-confirm"),
    # api/user/password-reset-complete/
    path("password-reset-complete/", SetNewPassword.as_view(), name="password-reset-complete"),
    # api/user/refresh-token/
    path("refresh-token/", CustomTokenRefreshView.as_view(), name="refresh_token"),
]
