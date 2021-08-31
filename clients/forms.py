from django import forms
from django.forms import ModelForm, Textarea
from . import models


class NewTicketForm(ModelForm):
    class Meta:
        model = models.SupportRequest
        fields = ('title', 'description', 'client_project')


class SupportRequestFilesForm(forms.ModelForm):
    class Meta:
        model = models.SupportRequestFiles
        fields = ('file', 'support_request')
