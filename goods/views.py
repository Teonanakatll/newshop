from django.shortcuts import render

from goods.models import Product


def catalog(request):

    goods = Product.objects.all()

    context = {
        "title": "Home - Каталог",
        "goods": goods,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    prod = Product.objects.get(slug=product_slug)

    context = {
        "product": prod,
    }

    return render(request, "goods/product.html", context)
