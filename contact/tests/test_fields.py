from django.test import TestCase
from django.forms import fields as django_fields

from .. import fields


class TestFields(TestCase):

    def test_all_fields_present(self):
        all_django_fields = set(django_fields.__all__)
        all_custom_fields = set(fields.__all__)
        self.assertTrue(all_django_fields.issubset(all_custom_fields))

        for field in all_custom_fields:
            custom_field = getattr(fields, field)
            django_field = getattr(django_fields, field, None)
            if django_field is not None:
                self.assertTrue(issubclass(custom_field, django_field))
            else:
                self.assertTrue(issubclass(custom_field, django_fields.Field))

    def test_init_widget_kwargs(self):
        # Normal django field behaviour
        with self.assertRaises(TypeError):
            django_fields.Field(attrs={})

        # But no exception raise with our fields
        attrs = {'foo': 'bar'}
        instance = fields.Field(attrs=attrs)

        # widget should now have foo=bar
        self.assertEqual(instance.widget.attrs, attrs)

    def test_prefix_clean_value(self):
        phone_number = fields.IntegerField(prefix='+44')
        value = phone_number.clean('01234567890')
        self.assertEqual(value, '+441234567890')
