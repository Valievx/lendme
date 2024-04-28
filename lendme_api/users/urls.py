from django.urls import path

app_name = "user"

urlpatterns = [
    path("api/user/login/", ..., name="login"),
    path("api/user/register/", ..., name="register"),
    path('api/user/send_sms/', ..., name='send_sms'),
    path("api/user/confirm_phone/", ..., name="confirm_phone"),
    path("api/user/profile/", ..., name="profile"),
    path("api/user/profile/update/", ..., name="profile_update"),
    path("api/user/password/reset/", ..., name="reset_user_password"),
    path("api/user/upload-image/", ..., name="upload_profile_image"),
    path("api/user/refresh-token/", ..., name="refresh_token"),
]
