from django.urls import path
from cursos.views import CursoDetailView, CursoListView, CursoCreateView


urlpatterns = [
    path('cursos/', CursoListView.as_view(), name='curso_list'),
    path('<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('curso/add/', CursoCreateView.as_view(), name='curso_add'),
]
