from django.shortcuts import render, get_object_or_404
from forum.models import Topic
from .models import Information


def home(request):
    """
    Vista de inicio de la aplicación ``core``.

    Muestra los 5 temas más recientes del foro, incluyendo información
    relacionada con su autor y categoría.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    django.http.HttpResponse
        Renderiza la plantilla ``core/home.html`` con el contexto:

        - ``recent_topics``: queryset con los 5 últimos temas creados.

    Example
    -------
    .. code-block:: python

        # URL: /
        # Renderiza la vista principal mostrando últimos temas
        response = home(request)
    """
    recent_topics = Topic.objects.select_related('author', 'category').order_by('-created_at')[:5]
    return render(request, 'core/home.html', {
        'recent_topics': recent_topics
    })
    

def info(request, info_id):
    """
    Vista para mostrar un documento de información específico.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP.
    info_id : int
        ID primario del objeto :class:`core.models.Information` a recuperar.

    Returns
    -------
    django.http.HttpResponse
        Renderiza la plantilla ``core/information_base.html`` con el contexto:

        - ``infodoc``: instancia del modelo :class:`Information`.

    Raises
    ------
    django.http.Http404
        Si no existe un objeto ``Information`` con el ``info_id`` dado.

    Example
    -------
    .. code-block:: python

        # URL: /info/3/
        # Muestra el documento de información con ID = 3
        response = info(request, info_id=3)
    """
    info = get_object_or_404(Information, pk=info_id)
    return render(request, 'core/information_base.html', {'infodoc': info})
 


def info_init(request):
    """
    Vista para mostrar la lista inicial de documentos de información.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    django.http.HttpResponse
        Renderiza la plantilla ``core/information_init.html`` con el contexto:

        - ``infodocs``: queryset de todos los objetos :class:`Information`.

    Example
    -------
    .. code-block:: python

        # URL: /info/
        # Muestra todos los documentos de información disponibles
        response = info_init(request)
    """
    infodocs = Information.objects.all()
    return render(request, 'core/information_init.html', {'infodocs': infodocs})
