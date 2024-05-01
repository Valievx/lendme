from django.urls import path

from users.views import (login_view, RegisterView,
                         SmsCodeCreateView, SmsCodeVerificationView,
                         profile_view, profile_update_view,
                         reset_user_password_view, refresh_token_view)

urlpatterns = [
    # api/user/login/
    path("login/", login_view, name="login"),
    # api/user/register/
    path("register/", RegisterView.as_view(), name="register"),
    # api/user/send_sms/
    path('send_sms/', SmsCodeCreateView.as_view(), name='send_sms'),
    # api/user/confirm_phone/
    path("confirm_phone/", SmsCodeVerificationView.as_view(), name="confirm_phone"),
    # api/user/profile/
    path("profile/", profile_view, name="profile"),
    # api/user/profile/update/
    path("profile/update/", profile_update_view, name="profile_update"),
    # api/user/password/reset/
    path("password/reset/", reset_user_password_view, name="reset_user_password"),
    # api/user/refresh-token/
    path("refresh-token/", refresh_token_view, name="refresh_token"),
]
