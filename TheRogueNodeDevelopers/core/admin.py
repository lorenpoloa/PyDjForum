from django.contrib import admin
from .models import Information, InfoSection
from django import forms
from pagedown.widgets import AdminPagedownWidget

class AdminInformationForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())
    
    class Meta:
        model = Information
        fields = '__all__'

class InformationAdmin(admin.ModelAdmin):
    form = AdminInformationForm

class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Information, InformationAdmin)
admin.site.register(InfoSection, InfoSectionAdmin)