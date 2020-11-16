from django import template

register = template.Library()


@register.simple_tag
def string_to_list(listString):
    array = listString.strip('][').split(', ')
    return array
