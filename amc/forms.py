from django import forms
from django.forms import ModelForm

from . import models
from .models import AMCRenewal


class AMCRenewalForm(ModelForm):
    class Meta:
        model = AMCRenewal
        fields = '__all__'
        exclude = ('created_at', 'created_by', 'reference')
        widgets = {
            'date': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'dateinput'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(AMCRenewalForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['reference'].widget = forms.TextInput(attrs={'readonly': 'readonly'})


class AMCDocumentsForm(forms.ModelForm):
    class Meta:
        model = models.AMCDocuments
        fields = ('file', 'amc')
