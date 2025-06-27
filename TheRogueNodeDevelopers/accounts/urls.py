from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.custom_login, name='login'),  # Ahora en /accounts/login/
    path('register/', views.register, name='register'),
    path('logout/',views.custom_logout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #path('generate_captcha_svg/', views.generate_captcha_svg, name='generate_captcha_svg'),
    path('register/accounts/generate_captcha_svg/', views.generate_captcha_svg, name='generate_captcha_svg'),

    # Recuperación de contraseña
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url=reverse_lazy('accounts:password_reset_done')
         ),
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]