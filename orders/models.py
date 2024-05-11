from django.db import models

from goods.models import Product
from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(order_item.product_price() for order_item in self)

    def total_quantity(self):
        if self:
            return sum(order_item.quantity for order_item in self)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, verbose_name="Пользователь")
    created_timestamp = models.DateTimeField("Дата создания заказа", auto_now_add=True)
    phone_number = models.CharField("Номер телефона", max_length=20)
    requires_delivery = models.BooleanField("Требуется доставка", default=False)
    delivery_address = models.TextField("Адрес доставки", blank=True, null=True)
    payment_on_get = models.BooleanField("Оплата при получении", default=False)
    is_paid = models.BooleanField("Оплачено", default=False)
    status = models.CharField("Статус заказа", max_length=50, default="В обработке")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField("Название", max_length=150)
    price = models.DecimalField("Цена", max_digits=7, decimal_places=2)
    quantity = models.SmallIntegerField("Количество", default=0)
    create_timestamp = models.DateTimeField("Дата продажи", auto_now_add=True)

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderitemQueryset.as_manager()

    def product_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"