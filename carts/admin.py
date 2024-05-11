from django.contrib import admin

from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("product", "quantity", "created_timestamp")
    readonly_fields = ("created_timestamp",)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("get_username", "product", "quantity", "created_timestamp")
    list_filter = ("created_timestamp", "user", "product")

    def get_username(self, object):
        if object.user:
            return str(object.user)
        return str(object.session_key)