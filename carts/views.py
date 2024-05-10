from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from carts.models import Cart
from goods.models import Product
from carts.utils import get_user_carts


def cart_add(request):

    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    user_cart = get_user_carts(request)

    # рендерим шаблон в строку для передачи в ajax в виде json строки
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

    # HTTP_REFERER хранит путь откуда был сделан запрос, т. е. данный редирект вернет обратно на ту же страницу
    # return redirect(request.META['HTTP_REFERER'])


def cart_change(request):

    cart_id = request.POST.get('cart_id')
    new_quantity = request.POST.get('quantity')

    cart = Cart.objects.get(id=cart_id)

    if cart.quantity < int(new_quantity):
        message = "1 товар добавлен"
    else:
        message = "1 товар удалён"
    cart.quantity = new_quantity
    cart.save()

    user_carts = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_carts}, request=request
    )

    response_data = {
        "message": message,
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def cart_remove(request):

    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_carts = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_carts}, request=request
    )

    response_data = {
        "message": 'Товар удалён',
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
    # return redirect(request.META['HTTP_REFERER'])

