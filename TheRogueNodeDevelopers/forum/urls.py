from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('topic/new/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topic/<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<slug:slug>/reply/', views.PostCreateView.as_view(), name='post_create'),
]