from django import template
from django.forms.widgets import TextInput, EmailInput, Textarea

register = template.Library()


@register.simple_tag
def get_form_field_template(boundfield):
    if type(boundfield.field.widget) in [TextInput, EmailInput]:
        return 'includes/inputfield.html'
    elif type(boundfield.field.widget) == Textarea:
        return 'includes/textarea.html'
