from crum import get_current_user
from django.conf import settings
from django.db import models


# Create your models here.
from django.utils.datetime_safe import datetime


class Project(models.Model):

    class Meta:
        db_table = 'projects'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    logo = models.FileField(null=True, blank=True, upload_to='clients/')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()
        super(Project, self).save(*args, **kwargs)

        if not self.code:
            self.code = "P" + str(self.id)
            self.save()

    def __str__(self):
        return self.name