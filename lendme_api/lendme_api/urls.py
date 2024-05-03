from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = "lend_me"

router = DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("users.urls")),
    path("api/", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
         "swagger/",
         SpectacularSwaggerView.as_view(url_name="schema"),
         name="swagger",
     ),
    path(
         "redoc/",
         SpectacularRedocView.as_view(url_name="schema"),
         name="redoc",
     ),
    re_path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
