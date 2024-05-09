from rest_framework import routers
from django.urls import include, path
from views import ProductViewSet, AddressViewSet

router = routers.DefaultRouter()
router.register(r'deals', ProductViewSet)
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
