from django.contrib import admin
from django.urls import include, path

app_name = "lend_me"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    
]
