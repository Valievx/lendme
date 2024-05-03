from rest_framework import viewsets
from .models import (
    Product,
    Address,
    Deposite,
    Category,
    SubCategory1,
    SubCategory2,
    ProductDeposite,)
from .serializers import (
    ProductSerializer,
    AddressSerializer,
    ProductDepositeSerializer,
    DepositeSerializer,
    CategorySerializer,
    SubCategory1Serializer,
    SubCategory2Serializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    """Класс для работы с моделью Product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """Класс для работы с моделью Address."""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс для работы с моделью Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategory1ViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс для работы с моделью SubCategory1."""

    queryset = SubCategory1.objects.all()
    serializer_class = SubCategory1Serializer


class SubCategory2ViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс для работы с моделью SubCategory2."""

    queryset = SubCategory2.objects.all()
    serializer_class = SubCategory2Serializer


class ProductDepositeViewSet(viewsets.ModelViewSet):
    """Класс для работы с моделью ProductDeposite."""

    queryset = ProductDeposite.objects.all()
    serializer_class = ProductDepositeSerializer


class DepositeViewSet(viewsets.ModelViewSet):
    """Класс для работы с моделью Deposite."""

    queryset = Deposite.objects.all()
    serializer_class = DepositeSerializer
