from django.contrib import admin
from .models import Deals


@admin.register(Deals)
class DealsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "deal_period",
        "deal_amount",
        "confirm_deposite",
        "created_at",
    )
    search_fields = ("user",)