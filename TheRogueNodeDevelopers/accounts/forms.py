from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
# from captcha.fields import CaptchaField


# Obtiene el modelo de usuario configurado en el proyecto
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de usuarios.

    Hereda de :class:`django.contrib.auth.forms.UserCreationForm` y añade 
    un campo adicional de captcha para la verificación al registrar un usuario.

    Attributes
    ----------
    password1 : django.forms.CharField
        Campo para la contraseña, con un widget de tipo ``PasswordInput``.
    password2 : django.forms.CharField
        Campo para confirmar la contraseña, con un widget de tipo ``PasswordInput``.
    captcha_input : django.forms.CharField
        Campo adicional para introducir un código de verificación (captcha).

    Example
    -------
    .. code-block:: python

        form = CustomUserCreationForm(data={
            'username': 'usuario',
            'email': 'correo@ejemplo.com',
            'password1': 'contraseña123',
            'password2': 'contraseña123',
            'captcha_input': 'ABC123'
        })
        if form.is_valid():
            form.save()
    """

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha_input = forms.CharField(max_length=6, label='Código de verificación')

    class Meta(UserCreationForm.Meta):
        """
        Metadatos del formulario.

        Define el modelo y los campos utilizados para la creación de usuarios.

        Attributes
        ----------
        model : django.db.models.Model
            El modelo de usuario configurado en el proyecto.
        fields : list
            Campos incluidos en el formulario: ``username`` y ``email``.
        """
        model = User
        fields = ['username', 'email']


class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario para la modificación de usuarios existentes.

    Permite a los usuarios o administradores actualizar información
    relacionada con el perfil, como el avatar, biografía o enlace a GitHub.

    Attributes
    ----------
    Meta.model : CustomUser
        Modelo de usuario personalizado definido en ``models.py``.
    Meta.fields : list
        Lista de campos que pueden ser modificados en el perfil.

    Example
    -------
    .. code-block:: python

        user = CustomUser.objects.get(username='usuario')
        form = CustomUserChangeForm(instance=user, data={
            'username': 'nuevo_usuario',
            'email': 'nuevo@correo.com',
            'bio': 'Desarrollador Django'
        })
        if form.is_valid():
            form.save()
    """

    class Meta:
        """
        Metadatos del formulario.

        Define el modelo de usuario y los campos que serán editables.
        """
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio', 'role', 'github_profile']


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado.

    Extiende :class:`django.contrib.auth.forms.AuthenticationForm` y añade
    un campo adicional para la opción de "recordar sesión".

    Attributes
    ----------
    username : django.forms.CharField
        Campo que permite autenticación usando email o nombre de usuario.
    password : django.forms.CharField
        Campo de contraseña con widget de tipo ``PasswordInput``.
    remember_me : django.forms.BooleanField
        Checkbox opcional para mantener la sesión iniciada.

    Example
    -------
    .. code-block:: python

        form = CustomAuthenticationForm(data={
            'username': 'usuario',
            'password': 'contraseña123',
            'remember_me': True
        })
        if form.is_valid():
            user = form.get_user()
    """

    username = forms.CharField(
        label=_("Email or Username"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label=_("Remember me")
    )
