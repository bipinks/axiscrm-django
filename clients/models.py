from datetime import datetime, timedelta

from ckeditor.fields import RichTextField
from crum import get_current_user
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, connection
# Create your models here.
from django.utils import timezone

from my_lib.views import date_add_days, date_next_year


class Client(models.Model):
    class Meta:
        db_table = 'clients'
        verbose_name_plural = "Manage Clients"
        ordering = ['-id']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = models.ImageField(null=True, blank=True, upload_to='clients/', default='clients/client_default.png')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, related_name='+'
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    @property
    def total_tickets(self):
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) total_tokens FROM support_requests sr " \
                    "LEFT JOIN client_projects cp ON cp.id=sr.client_project_id " \
                    "WHERE cp.client_id=" + str(self.id)

            cursor.execute(query)
            row = cursor.fetchone()

        return str(row[0])

    def save(self, *args, **kwargs):
        # print(self)
        # username = self.data.get('extra_field')
        self.created_by = get_current_user()
        super(Client, self).save(*args, **kwargs)
        if not self.code:
            # and self._state.adding:
            self.code = "C" + str(self.id)
            self.save()

    def __str__(self):
        return self.name


TOKEN_STATUS = (
    ('0', 'Active'),
    ('1', 'Due For AMC Renewal'),
    ('2', 'Project setup in progress'),
    ('3', 'Closed'),
)


class ClientProject(models.Model):
    class Meta:
        db_table = 'client_projects'
        verbose_name_plural = "Client Projects"
        ordering = ['-id']

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    start_date = models.DateField()
    next_amc_date = models.DateField(default=date_next_year)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=TOKEN_STATUS, default='0')
    project_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    amc_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    @property
    def total_tickets(self):
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) total_tokens FROM support_requests sr " \
                    "LEFT JOIN client_projects cp ON cp.id=sr.client_project_id " \
                    "WHERE cp.id=" + str(self.id)

            cursor.execute(query)
            row = cursor.fetchone()

        return str(row[0])

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()
        super(ClientProject, self).save(*args, **kwargs)

    def __str__(self):
        return self.client.name + " | " + self.project.name


class ClientProjectDocument(models.Model):
    class Meta:
        db_table = 'client_project_documents'
        verbose_name_plural = "Manage Client Project Documents"

    client_project = models.ForeignKey(ClientProject, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField()
    file = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()
        super(ClientProjectDocument, self).save(*args, **kwargs)


TICKET_STATUS = (
    ('0', 'Pending'),
    ('1', 'Open'),
    ('2', 'Awaiting Business Inputs'),
    ('3', 'With Client Review'),
    ('4', 'Closed|Resolved'),
    ('5', 'Deferred'),
)

TICKET_TYPES = (
    ('1', 'Service Related'),
    ('2', 'Sales Related'),
    ('3', 'Billing Related'),
    ('4', 'Others')
)


class SupportRequest(models.Model):
    class Meta:
        db_table = 'support_requests'
        verbose_name_plural = "Support Requests"
        ordering = ['-id']

    ticket_no = models.CharField(max_length=255)
    ticket_type = models.CharField(max_length=255, choices=TICKET_TYPES, default='1')
    client_project = models.ForeignKey(ClientProject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255, default='')
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    status = models.CharField(max_length=255, choices=TICKET_STATUS, default='0')

    @property
    def created_by_logo(self):
        if self.created_by.is_staff:
            return "https://i.imgur.com/iNmBizf.jpg"

        else:
            return self.created_by.client.logo.url

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()

        if not self.ticket_no:
            ticket_cnt = SupportRequest.objects.filter(client_project=self.client_project).count()
            project_code = self.client_project.project.code
            client_code = self.client_project.client.code

            self.ticket_no = "TICKET/" + project_code + "/" + client_code + "/" + str(ticket_cnt + 1)
            self.save()
        super(SupportRequest, self).save(*args, **kwargs)

    def __str__(self):
        return self.ticket_no


class SupportRequestFiles(models.Model):
    class Meta:
        db_table = 'support_request_files'
        verbose_name_plural = "Support Request Files"

    support_request = models.ForeignKey(SupportRequest, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='TicketFiles/')


class SupportActivity(models.Model):
    class Meta:
        db_table = 'support_activities'
        verbose_name_plural = "Support Request Activities"

    support_request = models.ForeignKey(SupportRequest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    @property
    def created_by_logo(self):
        if self.created_by.is_staff:
            return "https://i.imgur.com/iNmBizf.jpg"
        else:
            return self.created_by.client.logo.url

    def save(self, *args, **kwargs):
        self.created_by = get_current_user()
        super(SupportActivity, self).save(*args, **kwargs)


class SupportRequestActivityFiles(models.Model):
    class Meta:
        db_table = 'support_request_activity_files'
        verbose_name_plural = "Support Request Activity Files"

    activity = models.ForeignKey(SupportActivity, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='TicketActivityFiles/')
