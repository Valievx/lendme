from django.urls import path

from users.views import (login_view, register_view,
                         send_sms_view, confirm_phone_view,
                         profile_view, profile_update_view,
                         reset_user_password_view, refresh_token_view)

urlpatterns = [
    # api/user/login/
    path("login/", login_view, name="login"),
    # api/user/register/
    path("register/", register_view, name="register"),
    # api/user/send_sms/
    path('send_sms/', send_sms_view, name='send_sms'),
    # api/user/confirm_phone/
    path("confirm_phone/", confirm_phone_view, name="confirm_phone"),
    # api/user/profile/
    path("profile/", profile_view, name="profile"),
    # api/user/profile/update/
    path("profile/update/", profile_update_view, name="profile_update"),
    # api/user/password/reset/
    path("password/reset/", reset_user_password_view, name="reset_user_password"),
    # api/user/refresh-token/
    path("refresh-token/", refresh_token_view, name="refresh_token"),
]
