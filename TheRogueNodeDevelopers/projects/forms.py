from django import forms
from accounts.models import CustomUser


class ProjectCreateForm(forms.Form):
    name = forms.CharField(max_length=100, label="Project Name")
    repository_url = forms.URLField(label="Repository URL", required=False)
    deck_link = forms.URLField(label="Deck Link", required=False)
    maintainer = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label="Maintainer",
        required=False,)
    description = forms.CharField(widget=forms.Textarea, label="Description", required=False)
    start_date = forms.DateField(label="Start Date", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="End Date", required=False, widget=forms.DateInput(attrs={'type': 'date'}))