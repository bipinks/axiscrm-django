from django import forms
from django.forms import ModelForm, Textarea
from . import models


class AMCRenewalForm(ModelForm):
    class Meta:
        model = models.AMCRenewal
        fields = ('date', 'description', 'client_project')


class AMCDocumentsForm(forms.ModelForm):
    class Meta:
        model = models.AMCDocuments
        fields = ('file', 'amc')
