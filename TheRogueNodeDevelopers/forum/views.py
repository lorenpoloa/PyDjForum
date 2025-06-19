from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Category, Topic, Post
from .forms import TopicForm, PostForm
from django.db.models import Q

class CategoryListView(ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            topic_count=Count('topics')
        ).order_by('name')

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forum/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topics = self.object.topics.select_related('author', 'category').annotate(
            post_count=Count('posts')
        ).order_by('-is_pinned', '-created_at')
        
        paginator = Paginator(topics, 10)
        page_number = self.request.GET.get('page')
        context['topics'] = paginator.get_page(page_number)
        return context

def search(request):
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
    
    return render(request, 'forum/search.html', {
        'form': form,
        'results': results
    })


class TagTopicListView(ListView):
    model = Topic
    template_name = 'forum/tag_topics.html'
    
    def get_queryset(self):
        return Topic.objects.filter(
            tags__slug=self.kwargs.get('tag_slug')
        ).select_related('author', 'category')

class CategoryListView(ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forum/category_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all()
        return context

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum/topic_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        context['form'] = PostForm()
        self.object.increment_views()
        return context

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'slug': self.object.slug})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        form.instance.author = self.request.user
        form.instance.topic = topic
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'slug': self.kwargs['slug']}) + f'#post-{self.object.id}'