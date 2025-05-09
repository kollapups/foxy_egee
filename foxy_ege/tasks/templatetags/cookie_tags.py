from django import template

register = template.Library()

@register.filter
def has_cookie_consent(request, cookie_group):
    cookie_name = f"cookieconsent_{cookie_group}"
    return request.COOKIES.get(cookie_name) == "accept"