from django import template
from django.http import QueryDict

register = template.Library()

@register.simple_tag
def query_pages(request, field, value):
    url_query = request.GET.copy()
    url_query[field] = value
    return url_query.urlencode()