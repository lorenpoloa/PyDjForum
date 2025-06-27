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


# Función para generar colores aleatorios en formato hexadecimal
def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


def generate_random_string(length=6):
    """Generar una cadena aleatoria de letras y números."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def generate_captcha_svg(request):

    width = 200  # Ancho de la imagen
    height = 80  # Altura de la imagen
    num_elements = 100  # Número de líneas y puntos a dibujar
    characterSize = "40px";
    characterSize2 = 20;
    # Generar un nuevo texto de captcha aleatorio
    captcha_text = generate_random_string()

    # Guardar el texto del captcha en la sesión para validación
    request.session['captcha_text'] = captcha_text

    # Crear el archivo SVG utilizando svgwrite
    dwg = svgwrite.Drawing(size=("200px", "80px"))

    # Definir un fondo blanco para el captcha
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#121212"))
    # Agregar líneas aleatorias
    for _ in range(num_elements):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = random_color()
        dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=color, stroke_width=random.randint(1, 3)))

    # Agregar puntos aleatorios
    for _ in range(num_elements // 2):
        x, y = random.randint(0, width), random.randint(0, height)
        color = random_color()
        dwg.add(dwg.circle(center=(x, y), r=random.randint(1, 5), fill=color))
    

    initposX = 20;
    count = 0;
    # Agregar el texto del captcha al SVG con algunas configuraciones
    #dwg.add(dwg.text(captcha_text, insert=(20, 50), font_size="40px", fill="black", font_family="Arial"))
    for character in captcha_text:
        count+=1;
        initposX+=characterSize2;
        initposY=50;
        dwg.add(dwg.text(character,
            insert=(initposX,initposY),
            stroke=random_color(),
            fill_opacity = 0.6,
            fill= random_color(),
            stroke_width=2,
            font_size=characterSize,
            font_weight="bold",
            font_family="Courier New")
        )
        if(count%3 == 0):
            dwg.add(dwg.text("c",
                insert=(initposX,initposY),
                stroke_width=2,
                stroke_opacity = 0.0,
                fill_opacity = 0.0,
                font_size='40px',
                font_weight="bold",
                font_family="Courier New")
            )
    # Retornar el SVG como respuesta HTTP
    response = HttpResponse(content_type="image/svg+xml")
    dwg.write(response)
    return response


    
def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        # Obtener el captcha ingresado por el usuario
        captcha_input = request.POST.get('captcha_input', '').strip()

        # Verificar si el captcha ingresado coincide con el almacenado en la sesión
        captcha_text = request.session.get('captcha_text')

        if form.is_valid() and captcha_input == captcha_text:
            # Si el captcha es válido, procesamos el registro del usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Redirigir a la página de inicio o a alguna página de éxito
            return redirect('accounts:login')
        else:
            # Si el formulario no es válido o el captcha no coincide, agregar un error
            if captcha_input != captcha_text:
                form.add_error('captcha_input', 'El código de verificación es incorrecto.')
            
            # Volver a renderizar la página con el formulario y los errores
            return render(request, 'accounts/signup.html', {'form': form})
    
    else:

        form = CustomUserCreationForm()

        return render(request, 'accounts/signup.html', {'form': form})

# class SignUpView(CreateView):
#     model = CustomUser
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('accounts:login')
#     template_name = 'accounts/signup.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'email', 'avatar', 'bio', 'role', 'github_profile']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el perfil. Verifica los datos.')
        return super().form_invalid(self, form)



# Vistas basadas en funciones para mayor control
def custom_login(request):
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
    request.session.flush()
    logout(request)
    return render(request, 'accounts/logout.html')  # Cambia esto por tu URL deseada
