from django.shortcuts import render
from forum.models import Topic

# Create your views here.
def home(request):
    recent_topics = Topic.objects.select_related('author', 'category').order_by('-created_at')[:5]
    return render(request, 'core/home.html', {
        'recent_topics': recent_topics
    })
    