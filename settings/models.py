from datetime import datetime

from crum import get_current_user
from django.conf import settings
from django.db import models

# Create your models here.

DATE_FORMATS = (
    ('0', 'd-m-Y (eg: 31-12-2021)'),
    ('1', 'Y-m-d (eg: 2021-12-31)'),
    ('2', 'm-d-Y (eg: 12-31-2021)'),
)

EMAIL_ENC_TYPES = (
    ('SSL', 'SSL'),
    ('TLS', 'TLS'),
)


class Settings(models.Model):
    class Meta:
        db_table = 'settings'
        verbose_name_plural = "App Settings"

    app_name = models.CharField(max_length=255, default="axisCRM")
    logo = models.ImageField(null=True, blank=True, upload_to='settings/', default='settings/app_logo.png')
    date_format = models.CharField(max_length=255, choices=DATE_FORMATS, default='1')
    powered_by_name = models.CharField(max_length=255, default="Direct Axis Technology LLC")
    powered_by_website = models.CharField(max_length=255, default="https://directaxistech.com")
    email_host = models.CharField(max_length=255, null=True, blank=True)
    email_user = models.CharField(max_length=255, null=True, blank=True)
    email_default_from = models.CharField(max_length=255, null=True, blank=True)
    email_pwd = models.CharField(max_length=255, null=True, blank=True)
    email_port = models.CharField(max_length=255, null=True, blank=True)
    email_enc_type = models.CharField(max_length=255, choices=EMAIL_ENC_TYPES, default='SSL')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()
        super(Settings, self).save(*args, **kwargs)

    def __str__(self):
        return self.app_name
