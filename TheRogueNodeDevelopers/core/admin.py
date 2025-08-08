from django.contrib import admin
from .models import Information
from django import forms
from pagedown.widgets import AdminPagedownWidget

class AdminInformationForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())
    
    class Meta:
        model = Information
        fields = '__all__'

class InformationAdmin(admin.ModelAdmin):
    form = AdminInformationForm

admin.site.register(Information, InformationAdmin)