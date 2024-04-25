from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.ForeignKey(
        "Address",
        verbose_name="Адрес",
        related_name="products",
        on_delete=models.CASCADE,
    )
    category = ...
    # metro = ...
    price = models.IntegerField()
    image = models.ImageField(upload_to="products/image_products")
    author = models.ForeignKey(
        "CustomUser",
        verbose_name="Автор",
        related_name="products",
        on_delete=models.CASCADE,
    )
    deposit = ...
    created_at = models.DateTimeField(auto_now_add=True)
    time_period = ...


class Address(models.Model):
    address = ...
    city = models.ChoicesField(
        choices=...,
    )
    metro = ...

    class Meta:
        ordering = ("city",)
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.city
