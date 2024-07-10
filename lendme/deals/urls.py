from rest_framework import routers
from django.urls import include, path
from views import DealsViewSet

router = routers.DefaultRouter()
router.register(r'deals', DealsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]