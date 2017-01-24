from django.forms import fields


class FieldAttrsMixin():
    """
    Form field mixin to allow passing of attrs to the field, which will construct as normal, but then pass the attrs
    through to the field's widget.  It means you can specify html attributes for the widget, without having to know
    what the widget type is, and simplifies the following syntax:
        my_field = CharField(widget=TextInput(attrs={'property': 'value'}))
    to:
        my_field = CharField(attrs={'property': 'value'})
    """

    def __init__(self, *pargs, **kwargs):
        attrs = kwargs.pop('attrs', None)
        prefix = kwargs.pop('prefix', None)

        super().__init__(*pargs, **kwargs)

        if attrs is not None:
            self.widget.attrs.update(attrs)

        if prefix is not None:
            self.widget.prefix = prefix

# Loop over all items in the django.form.fields module
for field_name in fields.__all__:
    field = getattr(fields, field_name)
    # Check it's actually a field, not some constant
    if issubclass(field, fields.Field):
        # Add to the global scope of this module, a newly created Field class, that inherits from the original field,
        # has the same name as the original field, but that also inherits from our mixin
        globals()[field_name] = type(field_name, (FieldAttrsMixin, field), {})
