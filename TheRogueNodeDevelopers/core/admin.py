from django.contrib import admin
from .models import Information
from .forms import InformationForm

class InformationAdmin(admin.ModelAdmin):
    form = InformationForm
    list_display = ('title', 'is_public')
    search_fields = ('title', 'content')
    list_filter = ('is_public',)

admin.site.register(Information, InformationAdmin)
