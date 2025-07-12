from django import forms
from .models import Information
from pagedown.widgets import PagedownWidget

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'content', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(),
        }