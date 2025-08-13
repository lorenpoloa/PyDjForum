from django.contrib import admin
from .models import Project, GitRepository, Maintainer, Deck
# Register your models here.

@admin.register(Maintainer)
class MaintainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'repository', 'role')
    search_fields = ('user__username', 'repository__name', 'role')
    list_filter = ('role', 'repository__name')

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('link',)
    search_fields = ('link',)
    list_filter = ('link',) 

@admin.register(GitRepository)
class GitRepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'created_at', 'updated_at')
    search_fields = ('name', 'url')
    list_filter = ('created_at', 'updated_at')  

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

