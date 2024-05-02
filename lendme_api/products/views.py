from rest_framework import viewsets
from .models import Product, Address
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    '''Класс для работы с моделью Product.'''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class AddressViewSet(viewsets.ModelViewSet):
    '''Класс для работы с моделью Address.'''
    queryset = Address.objects.all()
    serializer_class = ProductSerializer