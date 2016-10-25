from django.conf.urls import url
from . import views

app_name = 'contact'

urlpatterns = [
    url(r'^feedback/thanks$', views.FeedbackThanksView.as_view(), name='feedback_thanks'),
    url(r'^feedback/(?P<service>[-\w\d]+)/$', views.FeedbackView.as_view(), name='feedback_submit'),
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
]
