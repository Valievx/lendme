from rest_framework import serializers

from .models import Deals

class DealsSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Deals.'''
    class Meta:
        '''Метакласс для указания модели и полей для сериализации.'''
        model = Deals
        fields = ('product', 'deal_period', 'deal_amount')

