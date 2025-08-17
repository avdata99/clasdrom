from django.urls import path
from . import views

urlpatterns = [
    path('preinscripcion/', views.crear_preinscripcion, name='crear_preinscripcion'),
]
