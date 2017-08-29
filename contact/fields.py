from django.forms import fields
from django.forms import widgets
from django.utils import html
from django.forms.utils import flatatt


__all__ = list(fields.__all__)


class FieldAttrsMixin():
    """
    Form field mixin to allow passing of attrs to the field, which will construct as normal, but then pass the attrs
    through to the field's widget.  It means you can specify html attributes for the widget, without having to know
    what the widget type is, and simplifies the following syntax:
        my_field = CharField(widget=TextInput(attrs={'property': 'value'}))
    to:
        my_field = CharField(attrs={'property': 'value'})
    """

    def __init__(self, attrs=None, prefix=None, *pargs, **kwargs):

        super().__init__(*pargs, **kwargs)

        if attrs is not None:
            self.widget.attrs.update(attrs)

        if prefix is not None:
            self.widget.prefix = prefix

    def clean(self, value):
        value = super().clean(value)
        prefix = getattr(self.widget, 'prefix', None)
        if prefix is not None:
            value = "{0}{1}".format(prefix, value)
        return value

# Loop over all items in the django.form.fields module
for field_name in fields.__all__:
    field = getattr(fields, field_name)
    # Check it's actually a field, not some constant
    if issubclass(field, fields.Field):
        # Add to the global scope of this module, a newly created Field class, that inherits from the original field,
        # has the same name as the original field, but that also inherits from our mixin
        globals()[field_name] = type(field_name, (FieldAttrsMixin, field), {})


class CompanyInput(widgets.TextInput):
    pass


class CompanyField(CharField):

    widget = CompanyInput

    def __init__(self, button_label, button_attrs=None, *pargs, **kwargs):
        super().__init__(*pargs, **kwargs)

        self.widget.button_label = button_label

        if button_attrs is not None:
            self.widget.button_attrs = button_attrs
