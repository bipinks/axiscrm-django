from ckeditor.fields import RichTextField
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from . import models
from .models import Client


class ClientForm(ModelForm):
    username = forms.CharField(label='Login Username')

    class Meta:
        model = models.Client
        fields = '__all__'
        exclude = ('created_at', 'created_by', 'user')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance.pk is None:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('duplicate username')
        return username

    def clean_code(self):
        code = self.cleaned_data['code']
        if self.instance.pk is None:
            if Client.objects.filter(code=code).exists():
                raise forms.ValidationError('duplicate client code')
        return code

    def save(self, commit=False):
        if self.instance.pk is None:
            username = self.cleaned_data['username']
            user = User.objects.create_user(
                username=username,
                first_name=self.cleaned_data['name'],
                is_staff=1,
                email=self.cleaned_data['email'],
                password='Daxis@217')
            self.instance.user = user

        return super(ClientForm, self).save(commit=True)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('username', None)
            self.fields['code'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

    # def __init__(self, *args, **kwargs):
    #     super(ClientForm, self).__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })


class NewTicketForm(ModelForm):
    class Meta:
        model = models.SupportRequest
        fields = ('title', 'description', 'client_project')
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'client_project': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super(NewTicketForm, self).__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })


class SupportRequestFilesForm(forms.ModelForm):
    class Meta:
        model = models.SupportRequestFiles
        fields = ('file', 'support_request')
