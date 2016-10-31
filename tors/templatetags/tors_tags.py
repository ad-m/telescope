from django import template

register = template.Library()


@register.filter
def is_ipv4(value):
    return not value.startswith('[')
