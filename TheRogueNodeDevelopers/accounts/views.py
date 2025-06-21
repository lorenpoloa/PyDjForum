from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'



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
