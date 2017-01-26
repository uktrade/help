from django import template
from django.forms.widgets import (
    TextInput, EmailInput, Textarea, Select, NumberInput, CheckboxInput, RadioSelect, URLInput
)

from ..fields import CompanyInput

register = template.Library()


@register.simple_tag
def get_form_field_template(boundfield):
    if type(boundfield.field.widget) == TextInput:
        return './includes/inputs/text.html'
    elif type(boundfield.field.widget) == EmailInput:
        return './includes/inputs/email.html'
    elif type(boundfield.field.widget) == NumberInput:
        return './includes/inputs/number.html'
    elif type(boundfield.field.widget) == URLInput:
        return './includes/inputs/url.html'
    elif type(boundfield.field.widget) == CheckboxInput:
        return './includes/inputs/checkbox.html'
    elif type(boundfield.field.widget) == Select:
        return './includes/inputs/selectfield.html'
    elif type(boundfield.field.widget) == Textarea:
        return './includes/inputs/textarea.html'
    elif type(boundfield.field.widget) == RadioSelect:
        return './includes/inputs/radio.html'
    elif type(boundfield.field.widget) == CompanyInput:
        return './includes/inputs/company.html'
    else:
        return './includes/inputs/base.html'


@register.filter
def next(array, current_index):
    """
    Returns the next element of the list using the current index
    """
    return array[int(current_index) + 1]


@register.filter
def previous(array, current_index):
    """
    Returns the previous element of the list using the current index
    """
    return array[int(current_index) - 1]
