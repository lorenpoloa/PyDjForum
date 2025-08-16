from django.db import models


class InfoSection(models.Model):
    """
    Modelo para agrupar información en secciones.

    Este modelo permite organizar los objetos :class:`Information` en categorías
    o secciones temáticas.

    Attributes
    ----------
    name : django.db.models.CharField
        Nombre de la sección. Máximo 100 caracteres.
    description : django.db.models.TextField
        Descripción breve de la sección.

    Methods
    -------
    __str__() -> str
        Retorna el nombre de la sección como representación en cadena.

    Example
    -------
    .. code-block:: python

        section = InfoSection.objects.create(
            name="Documentación",
            description="Sección para manuales y guías"
        )
        print(section)  # salida: Documentación
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        """
        Representación en cadena del objeto ``InfoSection``.

        Returns
        -------
        str
            Retorna el nombre de la sección.
        """
        return self.name


class Information(models.Model):
    """
    Modelo que representa un bloque de información.

    Este modelo guarda contenido textual con título, estado de visibilidad 
    y relación opcional con una sección (:class:`InfoSection`).

    Attributes
    ----------
    title : django.db.models.CharField
        Título de la información. Máximo 200 caracteres.
    content : django.db.models.TextField
        Texto completo del contenido.
    is_public : django.db.models.BooleanField
        Indica si la información es pública. Por defecto ``True``.
    info_section : django.db.models.ForeignKey
        Relación opcional con una sección de información. 
        ``related_name='information'``.

    Methods
    -------
    __str__() -> str
        Retorna el título junto con el estado de visibilidad (público/privado).

    Example
    -------
    .. code-block:: python

        section = InfoSection.objects.create(
            name="Tutoriales",
            description="Guías paso a paso"
        )

        info = Information.objects.create(
            title="Instalación de Django",
            content="Contenido detallado...",
            is_public=True,
            info_section=section
        )

        print(info)  
        # salida: Instalación de Django - Public
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    info_section = models.ForeignKey(
        InfoSection,
        on_delete=models.CASCADE,
        related_name='information',
        null=True,
        blank=True
    )   
    
    def __str__(self):
        """
        Representación en cadena del objeto ``Information``.

        Returns
        -------
        str
            Retorna el título y el estado de visibilidad (``Public`` o ``Private``).
        """
        return f"{self.title} - {'Public' if self.is_public else 'Private'}"
