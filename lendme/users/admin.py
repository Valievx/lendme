from django.contrib import admin

from .models import CustomUser, Favorite, Review


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone_number",
    )
    search_fields = ("email",)
    list_filter = ("email",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
    )
    search_fields = ("user",)
    list_filter = ("user",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "seller",
        "raiting",
        "comment",
        "created_at",
    )
    search_fields = ("client",)
    list_filter = ("client",)
