from django.shortcuts import get_object_or_404, render
from .models import Project
# Create your views here.


def project_list(request, pk=None):
    projects = Project.objects.all()
    project = None
    if pk:
        project = get_object_or_404(Project, pk=pk)
    
    return render(request, 'projects/projects_base.html', {
        'projects': projects,
        'project': project
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/projects_base.html', {'project': project})


class ProjectCreateView:
    def get(self, request):
        # Aquí iría la lógica para mostrar el formulario de creación de un proyecto
        return render(request, 'projects/project_form.html')

    def post(self, request):
        # Aquí iría la lógica para procesar el formulario de creación de un proyecto
        # Reemplazar con la lógica real
        return render(request, 'projects/project_form.html', {'success': True})