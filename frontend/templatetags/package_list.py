from django import template
from django.core.paginator import Page
register = template.Library()


@register.inclusion_tag("templatetags/package_list.html")
def package_list(page: Page):
    return {"page": page}
