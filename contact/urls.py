from django.conf.urls import url
from .generics.views import DITHelpView, DITThanksView
from .views import common, custom, api, old


app_name = 'contact'

# Basic non-form/API views
urlpatterns = [
    url(r'^ping\.json$', common.PingView.as_view(), name='ping'),
    url(r'^companies/$', api.company_detail_api, name='company_api'),
]

# Old redirected views
urlpatterns += [
    url(r'^feedback/(?P<service>[-\w\d]+)/?$', old.FeedbackRedirectView.as_view(), name='feedback_submit'),
    url(r'^triage/(?P<service>[-\w\d]+)/?$', old.TriageRedirectView.as_view(), name='triage_submit'),
]

# Dedicated service/form specific views
urlpatterns += [
    url(r'^soo/TriageForm/thanks?$', custom.TriageThanks.as_view(), name='triage_thanks'),
]

# Generic catch-all views that can figure out what form to serve
urlpatterns += [
    url(r'^(?P<service>[-\w\d]+)/?$', common.InterstitialContactView.as_view(), name='interstitial'),
    url(r'^(?P<service>[-\w\d]+)/(?P<form_name>[-\w\d]+)/?$',
        common.DefaultHelpView.as_view(),
        name='generic_submit'),
    url(r'^(?P<service>[-\w\d]+)/(?P<form_name>[-\w\d]+)/thanks/?$',
        common.DefaultThanksView.as_view(),
        name='generic_thanks'),
]
