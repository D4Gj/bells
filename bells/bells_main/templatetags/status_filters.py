# templatetags/status_filters.py
from django import template

register = template.Library()

STATUS_BELL = {
    "READY_TO_TRANSFER": "Готов к передаче",
    "IN_REQUEST_FOR_APPROVAL": "В заявке на согласование",
    "IN_USE": "Используется",
    "BELL_MISSING": "Не хватает колокола",
}


@register.filter(name="translate_status")
def translate_status(status):
    return STATUS_BELL.get(status, status)
