from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('infoinit/', views.info_init, name='info_init'),
    path('infoinit/info/<int:info_id>/', views.info, name='info'),
]