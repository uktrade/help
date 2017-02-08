from django import forms

from .generics.forms import DITHelpForm
from .meta import choices, label, help_text, regex, placeholder
from . import fields


class FeedbackForm(DITHelpForm):
    title = "Help us improve this service"
    subtitle = "We would love to hear your thoughts, concerns or problems with any aspects of the service so we\
                can improve it"

    content = forms.CharField(label="Feedback", required=True, widget=forms.Textarea)


class TriageForm(DITHelpForm):

    subtitle = "Application via Department for International Trade"
    submit_text = "Apply to join"

    contact_name = fields.CharField(required=True, label=label.CONTACT_NAME, attrs={'data-validate': 'name'})
    contact_email = fields.EmailField(required=True, label=label.CONTACT_EMAIL, attrs={'data-validate': 'email'})
    email_pref = fields.BooleanField(required=False, label=label.EMAIL_PREFERENCE)
    company_name = fields.CharField(required=True, attrs={'data-validate': 'company'},
                                    help_text=help_text.COMPANY_NAME)
    soletrader = fields.BooleanField(required=False, label=label.TRIAGE_UNREGISTERED_COMPANY,
                                     attrs={'data-validate': 'soletrader'})
    company_number = fields.CharField(required=False, label=label.COMPANY_NUMBER, help_text=help_text.COMPANY_NUMBER,
                                      attrs={'class': 'form-control--medium', 'data-validate': 'company-number'})
    company_postcode = fields.CharField(required=True, label=label.TRIAGE_POSTCODE,
                                        attrs={
                                            'class': 'form-control--medium',
                                            'data-validate': 'postcode',
                                            'placeholder': placeholder.POSTCODE
                                        })
    website_address = fields.URLField(required=True, label=label.COMPANY_WEBSITE, help_text=help_text.COMPANY_WEBSITE,
                                      attrs={'placeholder': placeholder.URL, 'data-validate': 'url'})
    turnover = fields.ChoiceField(required=True, label=label.TRIAGE_SALES, choices=choices.TRIAGE_SALES_THRESHOLDS,
                                  widget=forms.RadioSelect(), attrs={'data-validate': 'turnover'},
                                  help_text=help_text.TRIAGE_TURNOVER)
    trademarked = fields.ChoiceField(required=True, label=label.TRIAGE_TRADEMARKED, choices=choices.BOOLEAN_YES_NO,
                                     widget=forms.RadioSelect(), attrs={'data-validate': 'trademark'},
                                     help_text=help_text.TRIAGE_TRADEMARKED)
    experience = fields.ChoiceField(required=True, label=label.TRIAGE_EXPERIENCE, choices=choices.TRIAGE_EXPERIENCE,
                                    widget=forms.RadioSelect(), attrs={'data-validate': 'export'})
    description = fields.CharField(required=True, widget=forms.Textarea, help_text=help_text.TRIAGE_DESCRIPTION,
                                   label=label.TRIAGE_DESCRIPTION, attrs={'data-validate': 'description'})
    contact_phone = fields.IntegerField(required=True, label=label.CONTACT_PHONE, prefix='+44',
                                        attrs={'data-validate': 'contact-number'})
    sku_count = fields.IntegerField(required=True, label=label.TRIAGE_SKU_NUMBER,
                                    help_text=help_text.TRIAGE_SKU_NUMBER,
                                    attrs={
                                        'class': 'form-control--medium',
                                        'placeholder': placeholder.SKU,
                                        'data-validate': 'sku'
                                    })

    def is_valid(self):
        super().is_valid()
        return True

    fieldsets = (
        ('Your business', {
            'fields': (
                ('company_name', 'company_number', 'soletrader', 'company_postcode'),
                'website_address',
            ),
        }),
        ('Business details', {
            'fields': (
                'turnover',
                'sku_count',
                'trademarked',
            )
        }),
        ('Your experience', {
            'fields': (
                'experience',
                'description',
            )
        }),
        ('Contact details', {
            'fields': (
                ('contact_name', 'contact_email', 'contact_phone', 'email_pref'),
            )
        }),
    )
