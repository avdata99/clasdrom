from django.urls import path
from aulas.views import AulaDetailView, AulaListView, AulaCreateView, AulaUpdateView


urlpatterns = [
    path('lista/', AulaListView.as_view(), name='aula_list'),
    path('<int:pk>/', AulaDetailView.as_view(), name='aula_detail'),
    path('add/', AulaCreateView.as_view(), name='aula_add'),
    path('<int:pk>/editar/', AulaUpdateView.as_view(), name='aula_edit'),

    path('foto/<int:pk>/eliminar/', AulaUpdateView.as_view(), name='eliminar_foto'),
    path('foto/<int:pk>/editar/', AulaUpdateView.as_view(), name='editar_foto'),
]
