from django.urls import path
from aulas.views import AulaDetailView, AulaListView


urlpatterns = [
    path('aula/', AulaListView.as_view(), name='aula_list'),
    path('<int:pk>/', AulaDetailView.as_view(), name='aula_detail'),
]
