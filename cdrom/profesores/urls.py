from django.urls import path
from profesores.views import ProfesorCreateView, ProfesorDetailView, ProfesorListView

urlpatterns = [
    path('', ProfesorListView.as_view(), name='profe_list'),
    path('<int:pk>/', ProfesorDetailView.as_view(), name='profe_detail'),
    path('profe/add/', ProfesorCreateView.as_view(), name='profe_add'),
]
