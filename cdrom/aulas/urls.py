from django.urls import path
from aulas.views import AulaDetailView, AulaListView, AulaCreateView, AulaUpdateView


urlpatterns = [
    path('', AulaListView.as_view(), name='aula_list'),
    path('<int:pk>/', AulaDetailView.as_view(), name='aula_detail'),
    path('aula/add/', AulaCreateView.as_view(), name='aula_add'),
    path('aulas/<int:pk>/editar/', AulaUpdateView.as_view(), name='aula_edit'),
]
