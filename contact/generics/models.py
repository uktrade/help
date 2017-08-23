from django.db import models


class DITHelpModel(models.Model):
    """
    Base Model that stores the basic info in the DITHelpModelForm, along with a 'created' timestamp.
    If you want to store form data locally, your model should inherit from this.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    contact_name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Name")
    contact_email = models.EmailField(blank=False, null=False, verbose_name="Email")
    originating_page = models.CharField(max_length=255, blank=True, null=False)
    service = models.CharField(max_length=63, blank=False, null=False)
