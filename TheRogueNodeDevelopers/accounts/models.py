from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para la aplicación ``accounts``.

    Hereda de :class:`django.contrib.auth.models.AbstractUser` y redefine 
    algunos campos, además de añadir atributos específicos como biografía,
    avatar, rol y perfil de GitHub.  
    Se utiliza el correo electrónico como campo principal de autenticación
    en lugar del nombre de usuario.

    Attributes
    ----------
    email : django.db.models.EmailField
        Dirección de correo electrónico única para cada usuario.
    bio : django.db.models.TextField
        Texto corto de hasta 500 caracteres con la biografía del usuario.
    avatar : django.db.models.ImageField
        Imagen de perfil del usuario. Por defecto se asigna ``avatars/default.png``.
    role : django.db.models.CharField
        Rol o título del usuario dentro del sistema (ej. "Administrador").
    github_profile : django.db.models.URLField
        Enlace al perfil de GitHub del usuario, opcional.
    USERNAME_FIELD : str
        Define el campo que se usará para autenticación. Aquí es ``email``.
    REQUIRED_FIELDS : list
        Campos obligatorios adicionales al crear un superusuario.
    Meta.verbose_name : str
        Nombre singular para el modelo en el administrador de Django.
    Meta.verbose_name_plural : str
        Nombre plural para el modelo en el administrador de Django.

    Methods
    -------
    __str__() -> str
        Retorna el correo electrónico del usuario como representación de texto.

    Example
    -------
    .. code-block:: python

        # Crear un nuevo usuario
        user = CustomUser.objects.create_user(
            email="correo@ejemplo.com",
            username="usuario123",
            password="contraseña_segura",
            bio="Desarrollador Django",
            role="Backend Developer",
            github_profile="https://github.com/usuario123"
        )

        print(user)  # salida: correo@ejemplo.com
    """

    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('biography'), max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        default='avatars/default.png'
    )
    
    # Campos adicionales para personalización del perfil
    role = models.CharField(max_length=100, blank=True)
    github_profile = models.URLField(blank=True)
    
    # Se redefine el campo principal de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        """
        Configuración de metadatos para el modelo ``CustomUser``.

        Attributes
        ----------
        verbose_name : str
            Nombre singular del modelo en el administrador de Django.
        verbose_name_plural : str
            Nombre plural del modelo en el administrador de Django.
        """
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        """
        Representación en cadena del objeto ``CustomUser``.

        Returns
        -------
        str
            Retorna el correo electrónico del usuario.
        """
        return self.email
