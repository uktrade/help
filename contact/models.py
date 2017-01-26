from django.db import models
from .generics.models import DITHelpModel

from .meta.choices import TRIAGE_SALES_THRESHOLDS, BOOLEAN_YES_NO, TRIAGE_EXPERIENCE


class FeedbackModel(DITHelpModel):
    class Meta:
        verbose_name = "Feedback Submission"
        verbose_name_plural = "Feedback Submissions"

    content = models.TextField(null=False, blank=False)


class TriageModel(DITHelpModel):
    class Meta:
        verbose_name = "Triage Submission"
        verbose_name_plural = "Triage Submissions"

    company_name = models.CharField(max_length=255, null=False, blank=False)
    soletrader = models.BooleanField(null=False, default=False)
    company_number = models.CharField(max_length=32, null=False, blank=False)
    company_postcode = models.CharField(max_length=32, null=False, blank=False)
    website_address = models.URLField(null=False, blank=False)
    turnover = models.CharField(max_length=10, null=False, blank=False, choices=TRIAGE_SALES_THRESHOLDS, default='')
    sku_count = models.IntegerField(null=False, blank=False)
    trademarked = models.CharField(max_length=10, null=False, blank=False, choices=BOOLEAN_YES_NO, default='')
    experience = models.CharField(max_length=16, null=False, blank=False, choices=TRIAGE_EXPERIENCE, default='')
    description = models.TextField(null=False, blank=False)
    contact_phone = models.CharField(max_length=16, null=False, blank=True)
    email_pref = models.BooleanField(null=False, default=False)
