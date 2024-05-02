from rest_framework import serializers

from .models import Product, Address

class ProductSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Product.'''
    class Meta:
        '''Метакласс для указания модели и полей для сериализации.'''
        model = Product
        fields = ('title', 'description',
                  'address', 'category',
                  'price', 'image', 'author')
        

class AdressSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Adress.'''
    class Meta:
        ''' Метакласс для указания модели и полей для сериализации.'''
        model = Address
        fields = ('address', 'city', 'metro')