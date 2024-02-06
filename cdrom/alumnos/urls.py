from django.urls import path
from .views import AlumnoCreateView, AlumnoDetailView, AlumnoListView

urlpatterns = [
    # ... your other URL patterns ...
    path('alumnos/', AlumnoListView.as_view(), name='alumno_list'),
    path('alumnos/add/', AlumnoCreateView.as_view(), name='alumno_add'),
    path('alumnos/<int:pk>/', AlumnoDetailView.as_view(), name='alumno_detail'),
    # ...
]
