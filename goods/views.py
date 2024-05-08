from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, get_list_or_404

from goods.models import Product
from goods.utils import q_search


def catalog(request, category_slug=None):
    # фильтры
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    # поиск
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Product.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "title": "Home - Каталог",
        "page_obj": page_obj,
        "category_slug": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    prod = get_object_or_404(Product.objects.filter(slug=product_slug))

    context = {
        "product": prod,
    }

    return render(request, "goods/product.html", context)
