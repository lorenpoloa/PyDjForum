"""
Formularios para la aplicación de foro.

Incluye formularios para crear temas, publicaciones y realizar búsquedas.
"""

from django import forms
from .models import Topic, Post, Category, Tag
from pagedown.widgets import PagedownWidget

class TopicForm(forms.ModelForm):
    """
    Formulario para crear o editar un tema.

    Campos:
        title: Título del tema.
        content: Contenido del tema.
        category: Categoría seleccionada.
    """
    class Meta:
        model = Topic
        fields = ['title', 'content', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class PostForm(forms.ModelForm):
    """
    Formulario para crear una nueva publicación.

    Campos:
        content: Contenido de la publicación (con soporte Markdown).
    """
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': PagedownWidget(
                attrs={'rows': 10, 'placeholder': 'Escribe tu contenido en Markdown...'}
            ),
        }

class SearchForm(forms.Form):
    """
    Formulario para buscar temas en el foro.

    Campos:
        query: Texto de búsqueda.
        category: Categoría para filtrar.
        tags: Etiquetas para filtrar.
    """
    query = forms.CharField(required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )