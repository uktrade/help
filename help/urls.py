from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('contact.urls'), name="contact"),
]
