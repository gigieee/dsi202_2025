from django import template
from urllib.parse import parse_qs, urlencode


register = template.Library()

@register.filter
def remove_param(querystring, param):
    if not querystring:
        return ''
    parsed = parse_qs(querystring, keep_blank_values=True)
    parsed.pop(param, None)
    return urlencode(parsed, doseq=True)

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None