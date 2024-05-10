from django.shortcuts import render, redirect

from carts.models import Cart
from goods.models import Product


def cart_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    # HTTP_REFERER хранит путь откуда был сделан запрос, т. е. данный редирект вернет обратно на ту же страницу
    return redirect(request.META['HTTP_REFERER'])


    return render()

def cart_change(request, product_slug):
    ...
    return render()

def cart_remove(request, product_slug):
    ...
    return render()
