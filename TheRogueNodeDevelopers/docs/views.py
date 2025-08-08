from django.shortcuts import render, get_object_or_404
from .models import DocTopic, Documentation, ProcessState
from django.views.generic import ListView
from django.db.models import Count, Prefetch
from django.http import Http404


def documentation_init(request):

    return render(request, 'docs/documentation.html')


def documentation_development(request):
    documents = Documentation.objects.filter(
        process_state='DE',
        doc_topic__isnull=False
    ).select_related('doc_topic').order_by('doc_topic__name', 'title')

    context = {

        'title': 'Documentación de Desarrollo',
        'description': 'Documentación técnica del backend, frontend, APIs, dependencias y estructuras de carpetas.',
        'documents' : documents 
    }
    
    return render(request, 'docs/documentation_base.html', context)


def documentation_production(request):
    documents = Documentation.objects.filter(
        process_state='PR',
        doc_topic__isnull=False  # opcional: evitar documentos sin tópico
    ).select_related('doc_topic').order_by('doc_topic__name', 'title')

    context = {

        'title': 'Documentación de Usuario y Administrador',
        'description': 'Guías de uso, administración y manuales de las secciones ya desplegadas y en funcionamiento.',
        'documents' : documents 
    }
    
    return render(request, 'docs/documentation_base.html', context)


def documentation_detail(request, pk):
    docs = get_object_or_404(Documentation, pk=pk)
    return render(request, 'docs/_documentation_detail.html', {'docs': docs})
