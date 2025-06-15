from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Category, Topic, Post
from .forms import TopicForm, PostForm

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