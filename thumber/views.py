import os
from urllib.parse import urlparse

from django.views.generic.edit import View
from django.core.urlresolvers import resolve
from django.conf import settings
from django.http import JsonResponse

from .models import ContentFeedback
from .forms import ContentFeedbackForm


class ContentFeedbackMixin():

    satisfired_wording = 'Was this service useful?'
    yes_wording = 'Yes, thanks'
    no_wording = 'Not really'
    submit_wording = 'Send my feedback'
    thanks_wording = 'Thank you for your feedback'
    comment_placeholder = 'We are sorry to hear that. Would you tell us why?'

    def get_template_names(self):
        view = self.request.resolver_match

        view_components = view.view_name.split(':')
        view_specific_template = os.path.join('thumber', *view_components, 'feedback.html')
        app_specific_template = os.path.join('thumber', view_components[0], 'feedback.html')
        default_template = os.path.join('thumber', 'feedback.html')

        return [view_specific_template, app_specific_template, default_template]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        names = super().get_template_names()
        context['template_name'] = names[0]

        if self.request.method == 'POST' and self.request.POST.get('feedback_token', None) == 'sync':
            # feedback has been given via non AJAX request, add the 'thank you' message to the context
            context['thanks_wording'] = self.thanks_wording
        else:
            wordings = {
                'satisfied_wording': self.satisfired_wording,
                'yes_wording': self.yes_wording,
                'no_wording': self.no_wording,
                'comment_placeholder': self.comment_placeholder
            }
            context['form'] = ContentFeedbackForm(**wordings)
            context.update(wordings)
            context['submit_wording'] = self.submit_wording
            context['thanks_wording'] = self.thanks_wording

        return context

    def post(self, request):
        if request.POST.get('feedback_token', None) is not None:
            pk = request.POST.get('id', None)
            if pk is None or pk == '':
                # No PK, this means we need to create a new ContentFeedback object
                http_referer = self.request.META.get('HTTP_REFERER')
                sessionid = self.request.COOKIES[settings.SESSION_COOKIE_NAME]
                user_feedback = ContentFeedbackForm(data=request.POST).save(commit=False)
                user_feedback.url = http_referer
                user_feedback.page = self._get_view_from_url(http_referer)
                user_feedback.session = sessionid
            else:
                # PK given, so this ContentFeedback already exists and just needs the comment adding
                user_feedback = ContentFeedback.objects.get(pk=pk)
                user_feedback.comment = request.POST['comment']

            user_feedback.save()

            if request.POST.get('feedback', None) == 'sync':
                # Non-AJAX post, we've now done the processing, so return super's GET response
                return super().get(request)
            else:
                # AJAX submission, inform frontend the frontend the POST was successful, and give the id back so it can
                # be updated in a separate request
                return JsonResponse({"success": True, "id": user_feedback.id})
        else:
            return super().post(request)

    def _get_view_from_url(self, url):
        url_data = urlparse(url)
        host = url_data.netloc
        path = url_data.path
        viewname = resolve(path).view_name
        return viewname
