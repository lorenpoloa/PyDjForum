from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('init/', views.info_init, name='info_init'),
    path('init/info/', views.info, name='info_base'),
]