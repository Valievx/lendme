from rest_framework import serializers

from .models import (
    Product,
    Address,
    Deposite,
    ProductDeposite,
    Category,
    SubCategory1,
    SubCategory2,
)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product."""

    class Meta:
        """Метакласс для указания модели и полей для сериализации."""

        model = Product
        fields = (
            "title",
            "description",
            "address",
            "category",
            "price",
            "image",
            "author",
        )


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Adress."""

    class Meta:
        """Метакласс для указания модели и полей для сериализации."""

        model = Address
        fields = ("address", "city", "metro")


class DepositeSerializer(serializers.Serializer):
    """Сериализатор модели Deposit."""

    class Meta:
        model = Deposite
        fields = ("title", "slug")


class ProductDepositeSerializer(serializers.ModelSerializer):
    """Сериализатор модели ProductDeposite."""

    deposite = DepositeSerializer()

    class Meta:
        model = ProductDeposite
        fields = ("product", "deposite", "value")


class SubCategory2Serializer(serializers.Serializer):
    """Сериализатор модели SubCategory2."""

    class Meta:
        model = SubCategory2
        fields = ("title", "slug", "image")


class SubCategory1Serializer(serializers.Serializer):
    """Сериализатор модели SubCategory1."""

    subcategory2 = SubCategory2Serializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = SubCategory1
        fields = ("title", "slug", "image")


class CategorySerializer(serializers.Serializer):
    """Сериализатор модели Category."""

    subcategory1 = SubCategory1Serializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ("title", "slug", "image")
