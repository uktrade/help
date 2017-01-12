from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
    url(r'^(?P<service>[-\w\d]+)?$', views.InterstitialContactView.as_view(), name='interstitial'),
    url(r'^feedback/directory/$', views.DirectoryFeedbackView.as_view(), name='directory_submit'),
    url(r'^feedback/(?P<service>[-\w\d]+)/$', views.FeedbackView.as_view(), name='feedback_submit'),
    url(r'^triage/thanks/$', views.TriageThanksView.as_view(), name='triage_thanks'),
    url(r'^triage/(?P<service>[-\w\d]+)/$', views.TriageView.as_view(), name='triage_submit'),
]
