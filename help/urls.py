from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from ip_restriction import IpWhitelister


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('contact.urls'), name="contact"),
]
