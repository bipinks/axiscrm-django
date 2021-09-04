from ckeditor.fields import RichTextField
from django import forms
from django.forms import ModelForm, Textarea
from . import models


class NewTicketForm(ModelForm):
    class Meta:
        model = models.SupportRequest
        fields = ('title', 'description', 'client_project')
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'client_project': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(NewTicketForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class SupportRequestFilesForm(forms.ModelForm):
    class Meta:
        model = models.SupportRequestFiles
        fields = ('file', 'support_request')
