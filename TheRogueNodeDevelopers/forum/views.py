"""
Vistas para la aplicación de foro.

Incluye vistas basadas en clase y función para listar categorías, mostrar temas, crear temas y publicaciones, y buscar.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Category, Topic, Post
from .forms import TopicForm, PostForm, SearchForm
from django.db.models import Q, Count
from django.core.paginator import Paginator

class CategoryListView(ListView):
    """
    Vista para listar todas las categorías del foro.

    Atributos de clase:
        model: Modelo Category.
        template_name: Plantilla a renderizar.
        context_object_name: Nombre del contexto para la lista de categorías.
    """
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        """
        Devuelve el queryset de categorías con el conteo de temas asociados.
        """
        return Category.objects.annotate(
            topic_count=Count('topics')
        ).order_by('name')

class CategoryDetailView(DetailView):
    """
    Vista para mostrar el detalle de una categoría y sus temas.

    Atributos de clase:
        model: Modelo Category.
        template_name: Plantilla a renderizar.
    """
    model = Category
    template_name = 'forum/category_detail.html'
    
    def get_context_data(self, **kwargs):
        """
        Agrega los temas paginados de la categoría al contexto.
        """
        context = super().get_context_data(**kwargs)
        topics = self.object.topics.select_related('author', 'category').annotate(
            post_count=Count('posts')
        ).order_by('-is_pinned', '-created_at')
        
        paginator = Paginator(topics, 10)
        page_number = self.request.GET.get('page')
        context['topics'] = paginator.get_page(page_number)
        return context

def search(request):
    """
    Vista para buscar temas en el foro.

    Procesa el formulario de búsqueda y muestra los resultados en la plantilla base.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla con los resultados de búsqueda.
    """
    form = SearchForm(request.GET or None)
    results = []
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        tags = form.cleaned_data.get('tags')
        
        queryset = Topic.objects.all()
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
            
        if tags:
            queryset = queryset.filter(tags__in=tags).distinct()
            
        results = queryset.select_related('author', 'category')
    
    # Renderiza la plantilla base, no search.html
    return render(request, 'forum/base_forum.html', {
        'form': form,
        'results': results,
        'show_results': True,  # Variable para controlar si se muestran resultados
    })


class TagTopicListView(ListView):
    """
    Vista para listar los temas asociados a una etiqueta específica.

    Atributos de clase:
        model: Modelo Topic.
        template_name: Plantilla a renderizar.
    """
    model = Topic
    template_name = 'forum/tag_topics.html'
    
    def get_queryset(self):
        """
        Devuelve los temas filtrados por el slug de la etiqueta.
        """
        return Topic.objects.filter(
            tags__slug=self.kwargs.get('tag_slug')
        ).select_related('author', 'category')

class CategoryListView(ListView):
    """
    Vista para listar todas las categorías del foro (duplicada, revisar si es necesario).
    """
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    """
    Vista para mostrar el detalle de una categoría y sus temas (duplicada, revisar si es necesario).
    """
    model = Category
    template_name = 'forum/category_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        """
        Agrega los temas de la categoría al contexto.
        """
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all()
        return context

class TopicDetailView(DetailView):
    """
    Vista para mostrar el detalle de un tema y sus publicaciones.

    Atributos de clase:
        model: Modelo Topic.
        template_name: Plantilla a renderizar.
        slug_url_kwarg: Nombre del parámetro de URL para el slug.
        context_object_name: Nombre del contexto para el tema.
    """
    model = Topic
    template_name = 'forum/topic_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        """
        Agrega las publicaciones y el formulario de respuesta al contexto.
        """
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        context['form'] = PostForm()
        self.object.increment_views()
        return context

class TopicCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo tema en el foro.

    Atributos de clase:
        model: Modelo Topic.
        form_class: Formulario para el tema.
        template_name: Plantilla a renderizar.
    """
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_create.html'

    def form_valid(self, form):
        """
        Asigna el usuario autenticado como autor del tema.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Devuelve la URL de éxito tras crear el tema.
        """
        return reverse_lazy('forum:topic_detail', kwargs={'slug': self.object.slug})

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva publicación en un tema.

    Atributos de clase:
        model: Modelo Post.
        form_class: Formulario para la publicación.
    """
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        """
        Asigna el usuario autenticado y el tema a la publicación.
        """
        topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        form.instance.author = self.request.user
        form.instance.topic = topic
        return super().form_valid(form)

    def get_success_url(self):
        """
        Devuelve la URL de éxito tras crear la publicación, anclando al post.
        """
        return reverse_lazy('forum:topic_detail', kwargs={'slug': self.kwargs['slug']}) + f'#post-{self.object.id}'