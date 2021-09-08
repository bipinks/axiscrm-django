from crum import get_current_user
from django.conf import settings
from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime

from clients.models import ClientProject
from projects.models import Project


class AMCRenewal(models.Model):
    class Meta:
        db_table = 'amc_renewals'
        verbose_name_plural = "Manage AMC Renewals"

    reference = models.CharField(max_length=255)
    client_project = models.ForeignKey(ClientProject, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    renewed_date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()

        if not self.reference:
            renewal_cnt = AMCRenewal.objects.filter(client_project=self.client_project).count()
            project_code = self.client_project.project.code
            client_code = self.client_project.client.code

            self.reference = "AMC/" + project_code + "/" + client_code + "/" + str(renewal_cnt + 1)

        super(AMCRenewal, self).save(*args, **kwargs)

    def __str__(self):
        return self.reference


class AMCDocuments(models.Model):
    class Meta:
        db_table = 'amc_files'
        verbose_name_plural = "AMC Documents"

    amc = models.ForeignKey(AMCRenewal, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='AMCRenewalDocs/')
