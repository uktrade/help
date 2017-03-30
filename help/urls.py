from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings


urlpatterns = []

RESTRICT_IPS = getattr(settings, 'RESTRICT_IPS', None)

if RESTRICT_IPS is None:
    RESTRICT_IPS = os.environ.get('RESTRICT_IPS', '').lower() == 'true' or os.environ.get('RESTRICT_IPS') == '1'

if RESTRICT_IPS:
    # If we're restricting IPs, we want the admin site active to log in to,
    # but otherwise it is not needed, and shouldn't be accessible
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]

urlpatterns += [
    url(r'^', include('contact.urls'), name="contact"),
]
