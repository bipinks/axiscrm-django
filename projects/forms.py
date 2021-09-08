from django import forms
from django.forms import ModelForm

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('created_at', 'created_by')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def clean_code(self):
        code = self.cleaned_data['code']
        if self.instance.pk is None:
            if Project.objects.filter(code=code).exists():
                raise forms.ValidationError('duplicate code')
        return code

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['code'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

