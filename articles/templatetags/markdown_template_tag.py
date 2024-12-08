import markdown
from bleach import clean
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='MD')
def markdown_format(text):

    html = markdown.markdown(text, extensions=['extra', 'codehilite'])

    allowed_tags = [
        'p', 'b', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code'
    ]

    safe_html = clean(
        html,
        tags=allowed_tags,
        attributes={},
    )
    return mark_safe(safe_html)