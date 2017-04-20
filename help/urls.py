from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from ip_restriction import IpWhitelister


urlpatterns = []

ip = IpWhitelister()

if ip.RESTRICT_IPS and ip.ALLOW_ADMIN:
    # If we're restricting IPs, we want the admin site active to log in to,
    # but otherwise it is not needed, and shouldn't be accessible
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]

urlpatterns += [
    url(r'^', include('contact.urls'), name="contact"),
]
