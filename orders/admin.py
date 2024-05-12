from django.contrib import admin

from orders.models import OrderItem, Order


class OrderItemTabAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('order', 'name', 'price', 'quantity', 'create_timestamp')
    readonly_fields = ('create_timestamp',)
    extra = 0

class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = ('requires_delivery', 'status', 'payment_on_get', 'is_paid', 'created_timestamp')
    search_fields = ('requires_delivery', 'payment_on_get', 'is_paid', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'requires_delivery', 'status', 'payment_on_get', 'is_paid', 'created_timestamp')
    list_display_links = ('user', 'created_timestamp')
    # list_editable = ('status', 'is_paid')
    inlines = (OrderItemTabAdmin,)
    readonly_fields = ('created_timestamp',)

    search_fields = ('id', 'is_paid', 'user', 'created_timestamp')
    list_filter = ('status', 'user', 'is_paid', 'requires_delivery', 'payment_on_get')

    fields = (
        ('created_timestamp', 'user', 'phone_number'),
        ('requires_delivery', 'delivery_address'),
        ('status', 'is_paid', 'payment_on_get')
    )

@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'price', 'quantity', 'create_timestamp')
    list_display_links = ('order', 'name', 'price')
    readonly_fields = ('create_timestamp',)

    search_fields = ('order', 'product', 'name', 'create_timestamp')
    list_filter = ('order', 'name', 'create_timestamp')