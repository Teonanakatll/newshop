from django import template

from carts.utils import get_user_carts

register = template.Library()

@register.simple_tag()
# передаём request страницы
def user_carts(request):
    return get_user_carts(request)