from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('', views.documentation_init, name='documentation_init'),
    path('developers/index/', views.documentation_development, name='documentation_development'),
    path('production/index/', views.documentation_production, name='documentation_production'),

]