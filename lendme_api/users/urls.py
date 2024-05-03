from django.urls import path


from users.views import (
    LoginView,
    RegisterView,
    SmsCodeCreateView,
    SmsCodeVerificationView,
    PasswordResetView,
    CustomTokenRefreshView,
    SendEmailConfirmationTokenView,
    confirm_email_view
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
    path("confirm_email/", confirm_email_view, name="confirm_email"),
    # api/user/login/
    path("login/", LoginView.as_view(), name="login"),
    # api/user/password/reset/
    path("password/reset/", PasswordResetView.as_view(), name="reset_user_password"),
    # api/user/refresh-token/
    path("refresh-token/", CustomTokenRefreshView.as_view(), name="refresh_token"),
]
