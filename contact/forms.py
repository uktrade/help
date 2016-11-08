from django import forms

from .generics.forms import DITHelpForm
from .meta import choices, labels, help_text


class FeedbackForm(DITHelpForm):
    content = forms.CharField(label="Feedback", required=True, widget=forms.Textarea)


class TriageForm(DITHelpForm):
    company_name = forms.CharField(required=True, widget=forms.TextInput())
    company_type = forms.ChoiceField(required=True, choices=choices.TRIAGE_COMPANY_TYPES)
    company_number = forms.CharField(required=False, label=labels.COMPANY_NUMBER)
    website_address = forms.CharField(required=True, label=labels.COMPANY_WEBSITE)
    contact_name = forms.CharField(required=True, label=labels.CONTACT_NAME)
    contact_email = forms.EmailField(required=True, label=labels.CONTACT_EMAIL)
    sku_number = forms.IntegerField(required=True, label=labels.TRIAGE_SKU_NUMBER)
    sales = forms.ChoiceField(required=True, label=labels.TRIAGE_SALES, choices=choices.TRIAGE_SALES_THRESHOLDS)
    trademarked = forms.ChoiceField(required=True, label=labels.TRIAGE_TRADEMARKED, choices=choices.BOOLEAN_YES_NO)
    translation = forms.CharField(required=True, widget=forms.Textarea,
                                  label=labels.TRIAGE_TRANSLATION, help_text=help_text.TRIAGE_TRANSLATION)
    description = forms.CharField(required=True, widget=forms.Textarea,
                                  label=labels.TRIAGE_DESCRIPTION, help_text=help_text.TRIAGE_DESCRIPTION)

    field_order = [
        'company_name', 'contact_name', 'contact_email', 'website_address', 'company_type', 'company_number', 'sales',
        'sku_number', 'trademarked', 'translation', 'description'
    ]
