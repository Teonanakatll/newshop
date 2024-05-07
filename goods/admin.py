from django.contrib import admin

from . models import Category, Product


@admin.register(Category, Product)
class CategoriesAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "slug")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class ProductsAdmin(admin.ModelAdmin):
    """Продукты"""
    list_display = ("id", "name", "slug", "time_cteate", "time_update")
    list_filter = ("category__name", "time_create")
    search_fields = ("category__name", "time_create", "time_update")
    list_display_links = ("name", "time_create")
    prepopulated_fields = {"slug": ("name",)}
