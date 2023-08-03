from django.urls import path
from cursos.views import CursoDetailView, CursoListView, CursoCreateView


urlpatterns = [
    path('lista/', CursoListView.as_view(), name='curso_list'),
    path('<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('add/', CursoCreateView.as_view(), name='curso_add'),
]
