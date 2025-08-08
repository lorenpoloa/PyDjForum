from django.contrib import admin
from .models import DocTopic, Documentation
from django import forms
from pagedown.widgets import AdminPagedownWidget
from django.db import models

class DocumentationAdminForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())
    
    class Meta:
        model = Documentation
        fields = '__all__'

@admin.register(DocTopic)
class DocTopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    form = DocumentationAdminForm
    list_display = ('title', 'doc_topic')
    search_fields = ('title',)
    list_filter = ('doc_topic',)
