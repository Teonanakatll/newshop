from django.contrib import admin
from django.utils.safestring import mark_safe

from carts.admin import CartTabAdmin
from orders.admin import OrderTabAdmin
from . models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "get_avatar", "first_name", "last_name", "email")
    search_fields = ("id", "username", "first_name", "last_name", "email")
    list_display_links = ("username",)
    readonly_fields = ("get_avatar",)

    inlines = [CartTabAdmin, OrderTabAdmin]

    def get_avatar(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' height=100>")

