from django import forms
from django.core.urlresolvers import resolve

from .models import ContentFeedback


class ContentFeedbackForm(forms.ModelForm):

    class Meta:
        model = ContentFeedback
        fields = ['satisfied', 'comment']

    feedback_token = forms.CharField(initial='sync', widget=forms.HiddenInput())
    satisfied = forms.TypedChoiceField(
                    coerce=lambda x: x == 'True',
                    choices=((False, 'No'), (True, 'Yes')),
                    widget=forms.RadioSelect
                )

    def __init__(self, **kwargs):
        """
        The view may pass in some wording changes for the form.
        They will be passed in from the view, since this is outward interface for developers
        """

        satisfied_wording = kwargs.pop('satisfied_wording', None)
        yes_wording = kwargs.pop('yes_wording', None)
        no_wording = kwargs.pop('no_wording', None)
        comment_placeholder = kwargs.pop('comment_placeholder', None)

        super().__init__(**kwargs)

        if satisfied_wording is not None:
            self.fields['satisfied'].label = satisfied_wording
        if yes_wording is not None:
            choices = self.fields['satisfied'].choices
            new_choices = [choices[0], (True, yes_wording)]
            self.fields['satisfied'].choices = new_choices
        if no_wording is not None:
            choices = self.fields['satisfied'].choices
            new_choices = [(False, no_wording), choices[1]]
            self.fields['satisfied'].choices = new_choices
        if comment_placeholder is not None:
            self.fields['comment'].widget.attrs['placeholder'] = comment_placeholder
