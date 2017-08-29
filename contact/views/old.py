from django.views.generic import TemplateView, View, RedirectView
from django.core.urlresolvers import reverse


class FeedbackRedirectView(RedirectView):
    """
    Redirect from the old URL to the new generic-style URL
    """
    permanent = True

    def get_redirect_url(self, service):
        return reverse('contact:generic_submit', kwargs={'service': service, 'form_name': 'FeedbackForm'})


class TriageRedirectView(RedirectView):
    """
    Redirect from the old URL to the new generic-style URL
    """
    permanent = True

    def get_redirect_url(self, service):
        url = reverse('contact:generic_submit', kwargs={'service': service, 'form_name': 'TriageForm'})
        params = self.request.GET.urlencode()
        return "{0}?{1}".format(url, params)
