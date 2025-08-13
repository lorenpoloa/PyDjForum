from django.shortcuts import render, get_object_or_404
from forum.models import Topic
from .models import Information

# Create your views here.
def home(request):
    recent_topics = Topic.objects.select_related('author', 'category').order_by('-created_at')[:5]
    return render(request, 'core/home.html', {
        'recent_topics': recent_topics
    })
    

def info(request, info_id):
    info = get_object_or_404(Information, pk=info_id)
    # Assuming 'info' is a field in the Information model that contains the information text    
    
    return render(request, 'core/information_base.html', {'infodoc': info})
 


def info_init(request):
    infodocs = Information.objects.all()
    return render(request, 'core/information_init.html', {'infodocs': infodocs})
