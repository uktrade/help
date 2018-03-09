from django import forms
from django.conf import settings
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html

from .generics.forms import DITHelpForm, DITHelpModelForm
from .meta import choices, label, help_text, placeholder, validation
from .models import FeedbackModel, TriageModel
from . import fields


class FeedbackForm(DITHelpModelForm):
    title = "Help us improve great.gov.uk"
    subtitle = (
        "Give your feedback on the guidance and services on great.gov.uk. "
        "If something is wrong, give as much detail as you can."
    )

    class Meta:
        model = FeedbackModel
        exclude = []

    content = fields.CharField(
        label="Feedback",
        required=True,
        widget=forms.Textarea,
        attrs={
            'data-message': validation.FEEDBACK,
            'data-validate': 'feedback'
        },
        validators=[not_contains_url_or_email, no_html]
    )


class TriageForm(DITHelpModelForm):

    subtitle = "Application via Department for International Trade"
    submit_text = "Apply to join"

    def get_title(self):
        return self.request.GET.get('market', None)

    class Meta:
        model = TriageModel
        exclude = []

    company_name = fields.CompanyField(required=True,
                                       label=label.COMPANY_NAME,
                                       help_text=help_text.COMPANY_NAME,
                                       error_messages=validation.TRIAGE_COMPANY_NAME,
                                       attrs={
                                           'data-validate': 'company',
                                           'data-action': 'get-companies',
                                           'data-message': validation.TRIAGE_COMPANY_NAME['required'],
                                           'autocomplete': 'off',
                                           'class': 'form-dropdown-input'
                                       },
                                       button_label="Search Companies House",
                                       button_attrs={
                                           'class': 'button button-border button-border--blue button-medium\
                                           push--ends search-companies',
                                           'data-action': 'get-companies'
                                       })

    soletrader = fields.BooleanField(required=False,
                                     label=label.TRIAGE_UNREGISTERED_COMPANY,
                                     attrs={'data-validate': 'soletrader'})
    company_number = fields.CharField(required=False,
                                      label=label.COMPANY_NUMBER,
                                      attrs={
                                          'class': 'form-control--medium',
                                          'data-validate': 'company-number',
                                          'data-message': validation.TRIAGE_COMPANY_NUMBER['required']
                                      })
    company_postcode = fields.CharField(required=True,
                                        label=label.TRIAGE_POSTCODE,
                                        attrs={
                                            'class': 'form-control--medium',
                                            'data-validate': 'postcode',
                                            'placeholder': placeholder.POSTCODE,
                                            'data-message': validation.TRIAGE_COMPANY_POSTCODE['required']
                                        })

    email_pref = fields.BooleanField(required=False, label=label.EMAIL_PREFERENCE)
    contact_name = fields.CharField(required=True, label=label.CONTACT_NAME,
                                    error_messages=validation.TRIAGE_CONTACT_NAME,
                                    attrs={
                                        'data-validate': 'name',
                                        'data-message': validation.TRIAGE_CONTACT_NAME['required']
                                    })
    contact_email = fields.EmailField(required=True, label=label.CONTACT_EMAIL,
                                      error_messages=validation.TRIAGE_CONTACT_EMAIL,
                                      attrs={
                                          'data-validate': 'email',
                                          'data-message': validation.TRIAGE_CONTACT_EMAIL['required']
                                      })
    website_address = fields.URLField(required=True, label=label.COMPANY_WEBSITE, help_text=help_text.COMPANY_WEBSITE,
                                      error_messages=validation.TRIAGE_COMPANY_WEBSITE,
                                      attrs={
                                          'placeholder': placeholder.URL,
                                          'data-validate': 'url',
                                          'data-message': validation.TRIAGE_COMPANY_WEBSITE['required']
                                      })
    turnover = fields.ChoiceField(required=True, label=label.TRIAGE_SALES, choices=choices.TRIAGE_SALES_THRESHOLDS,
                                  widget=forms.RadioSelect(),
                                  error_messages=validation.TRIAGE_BUSINESS_TURNOVER,
                                  attrs={
                                      'data-validate': 'turnover',
                                      'data-message': validation.TRIAGE_BUSINESS_TURNOVER['required']
                                  },
                                  help_text=help_text.TRIAGE_TURNOVER)
    trademarked = fields.ChoiceField(required=True, label=label.TRIAGE_TRADEMARKED, choices=choices.BOOLEAN_YES_NO,
                                     widget=forms.RadioSelect(),
                                     error_messages=validation.TRIAGE_BUSINESS_TRADEMARK,
                                     attrs={
                                         'data-validate': 'trademark',
                                         'data-message': validation.TRIAGE_BUSINESS_TRADEMARK['required']
                                     },
                                     help_text=help_text.TRIAGE_TRADEMARKED)
    experience = fields.ChoiceField(required=True, label=label.TRIAGE_EXPERIENCE, choices=choices.TRIAGE_EXPERIENCE,
                                    widget=forms.RadioSelect(),
                                    error_messages=validation.TRIAGE_EXPERIENCE_EXPORT,
                                    attrs={
                                        'data-validate': 'export',
                                        'data-message': validation.TRIAGE_EXPERIENCE_EXPORT['required']
                                    })
    description = fields.CharField(required=True, widget=forms.Textarea, help_text=help_text.TRIAGE_DESCRIPTION,
                                   label=label.TRIAGE_DESCRIPTION,
                                   error_messages=validation.TRIAGE_EXPERIENCE_INTRODUCTION,
                                   attrs={
                                       'data-validate': 'description',
                                       'class': 'form-textarea--wide',
                                       'data-message': validation.TRIAGE_EXPERIENCE_INTRODUCTION['required']
                                   })
    contact_phone = fields.IntegerField(required=True, label=label.CONTACT_PHONE, prefix='+44',
                                        error_messages=validation.TRIAGE_CONTACT_PHONE,
                                        attrs={
                                          'data-validate': 'contact-number',
                                          'data-message': validation.TRIAGE_CONTACT_PHONE['required']
                                        })
    sku_count = fields.IntegerField(required=True, label=label.TRIAGE_SKU_NUMBER,
                                    help_text=help_text.TRIAGE_SKU_NUMBER,
                                    error_messages=validation.TRIAGE_BUSINESS_SKU,
                                    attrs={
                                        'class': 'form-control--medium',
                                        'placeholder': placeholder.SKU,
                                        'data-validate': 'sku',
                                        'data-message': validation.TRIAGE_BUSINESS_SKU['required']
                                    })

    @property
    def fieldsets(self):
        contact_details_fields = [
            'contact_name',
            'contact_email',
            'contact_phone',
            'email_pref',
        ]
        if settings.USE_CAPTCHA:
            contact_details_fields.append('captcha')
        return (
            (
                'Your business',
                {
                    'fields': (
                        'company_name',
                        'soletrader',
                        'company_number',
                        'company_postcode',
                        'website_address',
                    )
                }
            ),
            (
                'Business details',
                {
                    'fields': (
                        'turnover',
                        'sku_count',
                        'trademarked',
                    )
                }
            ),
            (
                'Your experience',
                {
                    'fields': (
                        'experience',
                        'description',
                    )
                }
            ),
            (
                'Contact details',
                {
                    'fields': contact_details_fields,
                }
            ),
        )
