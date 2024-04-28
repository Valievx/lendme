from django.db import models

from products.models import Deposite, Product
from users.models import CustomUser


class Deals(models.Model):
    """
    Модель сделок.
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Сделка",
        on_delete=models.CASCADE,
        related_name="deals",
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name="deals",
    )
    deal_period = models.DateField(
        verbose_name="Период сделки",
        help_text="Укажите период сделки",
    )
    deal_amount = models.IntegerField()
    confirm_deposite = models.ForeignKey(
        Deposite,
        verbose_name="Подтвержденный депозит",
        on_delete=models.CASCADE,
        related_name="deals",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
