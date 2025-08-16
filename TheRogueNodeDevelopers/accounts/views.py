from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import CustomUser
import svgwrite
import random
import string
import svgwrite


# ---------------------------------------------------------
# Funciones utilitarias
# ---------------------------------------------------------

def random_color():
    """
    Genera un color aleatorio en formato hexadecimal.

    Returns
    -------
    str
        Un color aleatorio en formato ``#RRGGBB``.
    """
    return f"#{random.randint(0, 0xFFFFFF):06x}"


def generate_random_string(length=6):
    """
    Genera una cadena aleatoria de letras y números.

    Parameters
    ----------
    length : int, optional
        Longitud de la cadena generada. Por defecto es ``6``.

    Returns
    -------
    str
        Cadena aleatoria compuesta por letras y dígitos.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# ---------------------------------------------------------
# Generación de Captcha
# ---------------------------------------------------------

def generate_captcha_svg(request):
    """
    Genera un captcha en formato SVG y lo almacena en la sesión del usuario.

    Este captcha combina líneas, puntos y texto aleatorio para dificultar 
    su lectura automatizada.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP. Se utiliza para almacenar el texto del 
        captcha en la sesión.

    Returns
    -------
    django.http.HttpResponse
        Respuesta HTTP con contenido ``image/svg+xml`` que contiene 
        el captcha generado.
    """
    width = 200  # Ancho de la imagen
    height = 80  # Altura de la imagen
    num_elements = 100  # Número de líneas y puntos a dibujar
    characterSize = "40px"
    characterSize2 = 20

    # Generar un nuevo texto de captcha aleatorio
    captcha_text = generate_random_string()
    request.session['captcha_text'] = captcha_text

    # Crear el archivo SVG
    dwg = svgwrite.Drawing(size=("200px", "80px"))

    # Fondo del captcha
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#121212"))

    # Líneas aleatorias
    for _ in range(num_elements):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = random_color()
        dwg.add(dwg.line(start=(x1, y1), end=(x2, y2),
                         stroke=color, stroke_width=random.randint(1, 3)))

    # Puntos aleatorios
    for _ in range(num_elements // 2):
        x, y = random.randint(0, width), random.randint(0, height)
        color = random_color()
        dwg.add(dwg.circle(center=(x, y), r=random.randint(1, 5), fill=color))

    # Texto del captcha
    initposX = 20
    count = 0
    for character in captcha_text:
        count += 1
        initposX += characterSize2
        initposY = 50
        dwg.add(dwg.text(
            character,
            insert=(initposX, initposY),
            stroke=random_color(),
            fill_opacity=0.6,
            fill=random_color(),
            stroke_width=2,
            font_size=characterSize,
            font_weight="bold",
            font_family="Courier New"
        ))
        if count % 3 == 0:
            dwg.add(dwg.text(
                "c",
                insert=(initposX, initposY),
                stroke_width=2,
                stroke_opacity=0.0,
                fill_opacity=0.0,
                font_size='40px',
                font_weight="bold",
                font_family="Courier New"
            ))

    # Retornar el SVG como respuesta HTTP
    response = HttpResponse(content_type="image/svg+xml")
    dwg.write(response)
    return response


# ---------------------------------------------------------
# Registro de usuario
# ---------------------------------------------------------

def register(request):
    """
    Vista para registrar un nuevo usuario con validación de captcha.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP que contiene los datos enviados 
        mediante el formulario de registro.

    Returns
    -------
    django.http.HttpResponse
        Renderiza la plantilla de registro en caso de error o 
        redirige al login si el registro es exitoso.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        captcha_input = request.POST.get('captcha_input', '').strip()
        captcha_text = request.session.get('captcha_text')

        if form.is_valid() and captcha_input == captcha_text:
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('accounts:login')
        else:
            if captcha_input != captcha_text:
                form.add_error('captcha_input', 'El código de verificación es incorrecto.')
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})


# ---------------------------------------------------------
# Vista de perfil
# ---------------------------------------------------------

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Vista para gestionar y actualizar el perfil de usuario.

    Hereda de :class:`django.views.generic.edit.UpdateView` y
    requiere que el usuario esté autenticado.

    Attributes
    ----------
    model : CustomUser
        Modelo de usuario personalizado.
    fields : list
        Lista de campos disponibles para editar.
    template_name : str
        Ruta de la plantilla utilizada para renderizar el perfil.
    success_url : str
        URL a la que se redirige tras una actualización exitosa.
    """

    model = CustomUser
    fields = ['username', 'email', 'avatar', 'bio', 'role', 'github_profile']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """
        Obtiene el usuario autenticado que será actualizado.

        Returns
        -------
        CustomUser
            El usuario actualmente autenticado.
        """
        return self.request.user
    
    def form_valid(self, form):
        """
        Acción ejecutada cuando el formulario es válido.

        Parameters
        ----------
        form : django.forms.ModelForm
            Formulario con los datos del perfil.

        Returns
        -------
        HttpResponseRedirect
            Redirige a la URL de éxito definida.
        """
        messages.success(self.request, 'Perfil actualizado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Acción ejecutada cuando el formulario contiene errores.

        Parameters
        ----------
        form : django.forms.ModelForm
            Formulario con los datos inválidos.

        Returns
        -------
        HttpResponse
            Renderiza nuevamente el formulario mostrando los errores.
        """
        messages.error(self.request, 'Error al actualizar el perfil. Verifica los datos.')
        return super().form_invalid(self, form)


# ---------------------------------------------------------
# Autenticación personalizada
# ---------------------------------------------------------

def custom_login(request):
    """
    Vista de inicio de sesión personalizada.

    Permite al usuario autenticarse mediante correo o nombre de usuario, 
    con la opción de mantener la sesión activa.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP con los datos del formulario de login.

    Returns
    -------
    django.http.HttpResponse
        Renderiza la plantilla de login o redirige a ``home`` si la 
        autenticación es exitosa.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Sesión expira al cerrar navegador
                messages.success(request, f"Bienvenido {user.username}!")
                return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def custom_logout(request):
    """
    Vista de cierre de sesión personalizada.

    Cierra la sesión del usuario, limpia los datos de la sesión 
    y renderiza la plantilla de logout.

    Parameters
    ----------
    request : django.http.HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    django.http.HttpResponse
        Renderiza la plantilla ``accounts/logout.html``.
    """
    request.session.flush()
    logout(request)
    return render(request, 'accounts/logout.html')
