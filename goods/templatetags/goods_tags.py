

from django import template
from django.utils.http import urlencode

from goods.models import Product, Category

register = template.Library()

@register.simple_tag()
def get_category():
    return Category.objects.all()

# через takes_context будут доступны все контекстные переменные
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
