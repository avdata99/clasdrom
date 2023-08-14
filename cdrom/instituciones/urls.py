from django.urls import path
from instituciones.views import InstitucionListView, InstitucionDetailView, InstitucionCreateView

urlpatterns = [
    path('lista/', InstitucionListView.as_view(), name='institucion_list'),
    path('<int:pk>/', InstitucionDetailView.as_view(), name='institucion_detail'),
    path('add/', InstitucionCreateView.as_view(), name='institucion_add'),
    # ... otras URL
]
