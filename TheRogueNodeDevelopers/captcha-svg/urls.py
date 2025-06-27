from django.urls import path
from . import views

app_name = 'captcha-svg'

urlpatterns = [

    path('register/captcha-svg/generate_captcha_svg/', views.generate_captcha_svg, name='generate_captcha_svg'),

]