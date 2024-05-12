from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from django.shortcuts import render

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                # Перед вызовом функции просмотра Django запускает транзакцию. Если ответ получен без проблем, Django
                # фиксирует транзакцию. Если представление вызывает исключение, Django откатывает транзакцию.
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Создать заказ
                        data = form.cleaned_data
                        order = Order.objects.create(user=user,phone_number=data['phone_number'],
                                                     requires_delivery=data['requires_delivery'],
                                                     delivery_address=data['delivery_address'],
                                                     payment_on_get=data['payment_on_get']
                                                     )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f"Недостаточное количество товара {name} на складе"
                                                      f"В наличии - {product.quantity}")

                            OrderItem.objects.create(order=order, product=product, name=name, price=price, quantity=quantity)
                            product.quantity -= quantity
                            product.save()

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                print(str(e))
                return redirect('orders:create_order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        # параметр initial начальные данные, инициализируем форму с начальными данными
        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
    }

    return render(request, 'orders/create-order.html', context)
