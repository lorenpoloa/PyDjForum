from django.contrib import admin
from django import forms
from .models import Category, Topic, Post, Tag
from django.db import models
from pagedown.widgets import AdminPagedownWidget

@admin.action(description='Marcar temas seleccionados como fijados')
def make_pinned(modeladmin, request, queryset):
    queryset.update(is_pinned=True)

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())
    
    class Meta:
        model = Post
        fields = '__all__'


class PostInline(admin.StackedInline):
    model = Post
    extra = 1
    fields = ('author', 'content', 'is_modified')
    readonly_fields = ('is_modified',)

class TopicAdmin(admin.ModelAdmin):
    actions = [make_pinned]
    list_display = ('title', 'author', 'category', 'created_at', 'views', 'is_pinned')
    list_filter = ('category', 'is_pinned', 'is_closed', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostInline]
    readonly_fields = ('views',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'topic_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def topic_count(self, obj):
        return obj.topics.count()
    topic_count.short_description = 'Temas'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('truncated_content', 'author', 'topic', 'created_at', 'is_modified')
    list_filter = ('created_at', 'is_modified')
    search_fields = ('content', 'author__username', 'topic__title')
    
    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Contenido'

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color_display')
    prepopulated_fields = {'slug': ('name',)}
    
    def color_display(self, obj):
        return f'<div style="width:20px; height:20px; background:{obj.color};"></div>'
    color_display.allow_tags = True
    color_display.short_description = 'Color'

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__username', 'post__content')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
#admin.site.register(Vote, VoteAdmin)