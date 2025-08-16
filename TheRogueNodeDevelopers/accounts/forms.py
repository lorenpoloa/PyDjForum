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
    un campo de captcha para la verificación adicional al registrar un usuario.

    Attributes
    ----------
    password1 : forms.CharField
        Campo para la contraseña, con un widget de tipo PasswordInput.
    password2 : forms.CharField
        Campo para confirmar la contraseña, con un widget de tipo PasswordInput.
    captcha_input : forms.CharField
        Campo adicional para introducir un código de verificación (captcha).
    """

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha_input = forms.CharField(max_length=6, label='Código de verificación')

    class Meta(UserCreationForm.Meta):
        """
        Metadatos del formulario.

        Define el modelo y los campos utilizados para la creación de usuarios.
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
        Lista de campos que pueden ser modificados.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio', 'role', 'github_profile']


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado.

    Extiende :class:`django.contrib.auth.forms.AuthenticationForm` y añade
    un campo adicional para la opción de "recordar sesión".

    Attributes
    ----------
    username : forms.CharField
        Campo que permite autenticación usando email o nombre de usuario.
    password : forms.CharField
        Campo de contraseña con widget de tipo PasswordInput.
    remember_me : forms.BooleanField
        Checkbox opcional para mantener la sesión iniciada.
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
