from django.contrib import admin
from .models import (Product,
                     Address,
                     ProductImages,
                     ProductDeposite,
                     Deposite,
                     Category,
                     SubCategory1, 
                     SubCategory2)

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1

class ProductDepositeInline(admin.TabularInline):
    model = ProductDeposite
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline, ProductDepositeInline]
    list_display = ("title", "description",
                     "address", "category",
                     "price", "author",
                     "time_period")
    search_fields = ["title", "description"]
    ordering = ["-created_at"]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address", "city", "metro")
    search_fields = ["address", "city", "metro"]

@admin.register(Deposite)
class DepositeAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "image")

@admin.register(SubCategory1)
class SubCategory1Admin(admin.ModelAdmin):
    list_display = ("title", "slug", "image", "category")

@admin.register(SubCategory2)
class SubCategory2Admin(admin.ModelAdmin):
    list_display = ("title", "slug",
                    "image", "subcategory1")


