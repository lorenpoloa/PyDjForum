"""
Modelos principales para la aplicación de foro.

Incluye las clases Tag, Category, Topic y Post para estructurar el sistema de foros.
"""

from django.db import models
from django import forms
from accounts.models import CustomUser
from django.urls import reverse
from django.utils.text import slugify

class Tag(models.Model):
    """
    Etiqueta para clasificar temas del foro.

    Attributes:
        name (str): Nombre de la etiqueta.
        slug (str): Slug único para la URL.
        color (str): Código HEX del color de la etiqueta.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#6c757d')  # Código HEX color

    def __str__(self):
        """Devuelve el nombre de la etiqueta."""
        return self.name

class Category(models.Model):
    """
    Representa una categoría del foro.

    Attributes:
        name (str): Nombre de la categoría.
        slug (str): Slug único para la URL.
        description (str): Descripción de la categoría.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        """Devuelve el nombre de la categoría."""
        return self.name

    def save(self, *args, **kwargs):
        """
        Guarda la categoría. Si no tiene slug, lo genera automáticamente a partir del nombre.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Devuelve la URL absoluta para el detalle de la categoría.
        """
        return reverse('forum:category_detail', kwargs={'slug': self.slug})

class Topic(models.Model):
    """
    Tema de discusión dentro de una categoría.

    Attributes:
        tags (ManyToMany[Tag]): Etiquetas asociadas al tema.
        title (str): Título del tema.
        slug (str): Slug único para la URL.
        content (str): Contenido del tema.
        author (CustomUser): Autor del tema.
        category (Category): Categoría a la que pertenece el tema.
        views (int): Número de visualizaciones.
        is_pinned (bool): Si el tema está fijado.
        is_closed (bool): Si el tema está cerrado.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.
    """
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='topics')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        """Devuelve el título del tema."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Guarda el tema. Si no tiene slug, lo genera automáticamente a partir del título y el pk.
        """
        if not self.slug:
            self.slug = slugify(f"{self.title[:200]}-{self.pk}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Devuelve la URL absoluta para el detalle del tema.
        """
        return reverse('forum:topic_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """
        Incrementa el contador de visualizaciones del tema.
        """
        self.views += 1
        self.save(update_fields=['views'])

class Post(models.Model):
    """
    Publicación o respuesta dentro de un tema.

    Attributes:
        content (str): Contenido de la publicación.
        author (CustomUser): Autor de la publicación.
        topic (Topic): Tema al que pertenece la publicación.
        created_at (datetime): Fecha de creación.
        updated_at (datetime): Fecha de última actualización.
        is_modified (bool): Indica si la publicación fue editada.
    """
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_modified = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        """Devuelve una representación de la publicación."""
        return f"Post by {self.author.username} in {self.topic.title}"

    def save(self, *args, **kwargs):
        """
        Guarda la publicación. Si ya existe, marca como modificada.
        """
        if self.pk:  # Si el post ya existe
            self.is_modified = True
        super().save(*args, **kwargs)