from rest_framework import viewsets

from .models import Deals
from .serializers import DealsSerializer


class DealsViewSet(viewsets.ModelViewSet):
    '''Класс для работы с моделью Deals.'''
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer