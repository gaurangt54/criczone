from django import template
register = template.Library()


@register.simple_tag()
def multiply(qty, price, *args, **kwargs):
    return qty * price
