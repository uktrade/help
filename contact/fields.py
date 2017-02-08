from django.forms import fields
from django.forms import widgets


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

# Loop over all items in the django.form.fields module
for field_name in fields.__all__:
    field = getattr(fields, field_name)
    # Check it's actually a field, not some constant
    if issubclass(field, fields.Field):
        # Add to the global scope of this module, a newly created Field class, that inherits from the original field,
        # has the same name as the original field, but that also inherits from our mixin
        globals()[field_name] = type(field_name, (FieldAttrsMixin, field), {})


class CompanyInput(widgets.HiddenInput):
    pass


class CompanyField(CharField):
    widget = CompanyInput
    company_name_widget = widgets.TextInput
    company_number_widget = widgets.TextInput
    soletrader_widget = widgets.CheckboxInput
    postcode_widget = widgets.TextInput

    def __init__(self, company_name_label, company_number_label, soletrader_label, postcode_label,
                 company_name_attrs=None, company_number_attrs=None, soletrader_attrs=None, postcode_attrs=None,
                 *pargs, **kwargs):

        super().__init__(*pargs, **kwargs)

        self.company_name_widget = self.company_name_widget()
        self.company_number_widget = self.company_number_widget()
        self.soletrader_widget = self.soletrader_widget()
        self.postcode_widget = self.postcode_widget()

        self.company_name_label = company_name_label
        self.company_number_label = company_number_label
        self.soletrader_label = soletrader_label
        self.postcode_label = postcode_label

        if company_name_attrs is not None:
            self.company_name_widget.attrs.update(company_name_attrs)

        if company_number_attrs is not None:
            self.company_number_widget.attrs.update(company_number_attrs)

        if soletrader_attrs is not None:
            self.soletrader_widget.attrs.update(soletrader_attrs)

        if postcode_attrs is not None:
            self.postcode_widget.attrs.update(postcode_attrs)
