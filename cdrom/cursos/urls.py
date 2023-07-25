from django.urls import path
from cursos.views import CursoDetailView, CursoListView


urlpatterns = [
    path('', CursoListView.as_view(), name='curso_list'),
    path('<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
]
