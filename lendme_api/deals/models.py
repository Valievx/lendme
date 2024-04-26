from django.db import models


class Deals(models.Model):
    """
    Модель сделок.
    """
    user = models.ForeignKey(
        "CustomUser",
        verbose_name="Сделка",
        on_delete=models.CASCADE,
        related_name="deals",
    )
    product = models.ForeignKey(
        "Product",
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name="deals",
    )
    deal_period = models.IntegerField()
    deal_amount = models.IntegerField()
    confirm_deposite = models.ForeignKey(
        "Deposite",
        verbose_name="Подтвержденный депозит",
        on_delete=models.CASCADE,
        related_name="deals",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
