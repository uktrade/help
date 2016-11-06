from django import template
from django.forms.widgets import TextInput, EmailInput, Textarea, Select, NumberInput

register = template.Library()


@register.simple_tag
def get_form_field_template(boundfield):
    if type(boundfield.field.widget) in [TextInput, EmailInput, NumberInput]:
        return 'includes/inputfield.html'
    elif type(boundfield.field.widget) == Select:
        return 'includes/selectfield.html'
    elif type(boundfield.field.widget) == Textarea:
        return 'includes/textarea.html'
