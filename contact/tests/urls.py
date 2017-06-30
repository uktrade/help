from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from .. import views
from ..generics.views import DITHelpView
from ..generics.forms import DITHelpForm

app_name = 'contact'


class BasicView(DITHelpView):
    form_class = DITHelpForm
    success_url = reverse_lazy('thanks')


urlpatterns = [
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
    url(r'^generic/(?P<service>[-\w\d]+)/$', BasicView.as_view(), name='generic'),
]
