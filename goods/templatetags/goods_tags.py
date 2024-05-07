from django import template
from goods.models import Product, Category

register = template.Library()

@register.simple_tag()
def get_category():
    return Category.objects.all()
