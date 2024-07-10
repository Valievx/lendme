from django.db import models

from users.models import CustomUser


class Product(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=100,
        unique=False,
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    address = models.ForeignKey(
        "Address",
        verbose_name="Адрес",
        related_name="products",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        "Category",
        verbose_name="Категория",
        related_name="products",
        on_delete=models.CASCADE,
    )
    # metro = ...
    price = models.IntegerField(
        verbose_name='Цена'
    )
    image = models.ImageField(upload_to="products/image_products")
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        related_name="products",
        on_delete=models.CASCADE,
    )
    deposit = ...
    created_at = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True)
    time_period = models.CharField(
        verbose_name="Период времени",
        max_length=20,
        choices=[
            ("Час", "Час"),
            ("Сутки", "Сутки"),
            ("Месяц", "Месяц"),
        ]
    )


class Address(models.Model):
    """
    Модель адрресов сдаваемой продукцией в аренду.
    """
    address = models.CharField(max_length=255, default="Заглушка адреса")
    city = models.CharField(max_length=100, default="Заглушка города")
    metro = models.CharField(max_length=100, default="Заглушка метро")

    class Meta:
        ordering = ("city",)
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.city


class ProductImages(models.Model):
    """
    Модель изображений продукта.
    """
    product = models.ForeignKey(
        "Product",
        verbose_name="Продукт",
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = ...


class ProductDeposite(models.Model):
    """
    Модель депозита продукта.
    """
    product = models.ForeignKey(
        "Product",
        verbose_name="Продукт",
        related_name="products_deposite",
        on_delete=models.CASCADE,
    )
    deposite = models.ForeignKey(
        "Deposite",
        verbose_name="Депозит",
        related_name="products_deposite",
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        verbose_name="Сумма депозита",
        unique=False,
        blank=True,
        default=0,
    )


class Deposite(models.Model):
    """
    Модель депозита.
    """
    title = models.CharField(
        verbose_name="Наименование депозита",
        max_length=35,
        unique=False,
    )
    slug = models.SlugField(
        verbose_name="Ссылка",
        max_length=35,
        unique=False,
    )


class Category(models.Model):
    """
    Модель категорий продуктов.
    """
    title = models.CharField(
        verbose_name="Наименование категории",
        max_length=35,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Ссылка",
        max_length=35,
        unique=False,
    )
    image = models.ImageField(
        verbose_name="Изображение категории",
        upload_to="categories/image_categories",
        unique=False,
        null=True,
        blank=True
    )


class SubCategory1(models.Model):
    """
    Модель подкатегорий продуктов.
    """
    title = models.CharField(
        verbose_name="Наименование подкатегории",
        max_length=35,
        unique=False,
    )
    slug = models.SlugField(
        verbose_name="Ссылка",
        max_length=35,
        unique=False,
    )
    image = models.ImageField(
        verbose_name="Изображение категории",
        upload_to="categories/image_subcategories1",
        unique=False,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name='subcategories1',
    )


class SubCategory2(models.Model):
    """
    Модель подкатегорий продуктов.
    """
    title = models.CharField(
        verbose_name="Наименование подкатегории",
        max_length=35,
        unique=False,
    )
    slug = models.SlugField(
        verbose_name="Ссылка",
        max_length=35,
        unique=False,
    )
    image = models.ImageField(
        verbose_name="Изображение категории",
        upload_to="categories/image_subcategories2",
        unique=False,
        null=True,
        blank=True
    )
    subcategory1 = models.ForeignKey(
        "SubCategory1",
        on_delete=models.CASCADE,
        related_name='subcategories2',
    )
