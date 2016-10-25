from django import forms

from .generics.forms import DITHelpForm


class FeedbackForm(DITHelpForm):
    content = forms.CharField(label="Feedback", required=True, widget=forms.Textarea)

    def get_body(self):
        content = self.cleaned_data.get('content')
        origin_page = self.cleaned_data.get('originating_page')
        if origin_page:
            content = self.cleaned_data.get('content')
            body = "User was on page:{0}\n\n{1}".format(origin_page, content)
        else:
            body = "{0}".format(content)
        return body
