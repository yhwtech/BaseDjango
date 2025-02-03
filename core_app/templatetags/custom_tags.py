from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_active(request, args):
    index = 0
    url_parent = args
    current_url = request.resolver_match.route
    split_url = current_url.split(sep="/")
    if ',' in args:
        split = args.split(',')
        url_parent = split[0]
        index = int(split[1])

    if index >= len(split_url) - 1:
        index = len(split_url)-1

    parent_route = split_url[index]
    return parent_route == url_parent


@register.filter
def is_active_by_url_name(request, url_name):
    current_url_name = request.resolver_match.url_name
    return current_url_name == url_name


@register.filter
def is_empty(value):
    return len(value) == 0


@register.filter
def days_remaining(start, days):
    try:
        actual = timezone.now()
        difference_days = (actual - start).days
        return difference_days

    except ValueError:
        return "Invalid date"

@register.filter
def month_name(month):
    months = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return months[month - 1] if 1 <= month <= 12 else ""