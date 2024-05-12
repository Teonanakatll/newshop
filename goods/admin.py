from django.contrib import admin
from django.utils.safestring import mark_safe

from . models import Category, Product


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "slug")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    """Продукты"""

    list_display = ("id", "name", "get_image", "discount", "time_create", "time_update")
    list_editable = ("discount",)
    list_filter = ("id","category__name", "time_create")
    search_fields = ("id", "category__name", "time_create", "time_update")
    list_display_links = ("name", "time_create")
    prepopulated_fields = {"slug": ("name",)}

    # Отобразить панель редактирования сверху
    save_on_top = True
    # Сохранить как новый обьект
    save_as = True

    fields = (
        "name",
        "category",
        ("quantity", "price", "discount"),
        "description",
        "slug",
        "get_image",
        "image",
    )

    readonly_fields = ("get_image",)

    def get_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' height=100>")

    get_image.short_description = "Фото товара"
