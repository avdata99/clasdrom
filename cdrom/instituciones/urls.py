from django.urls import path
from instituciones.views import InstitucionListView, InstitucionDetailView, InstitucionCreateView

urlpatterns = [
    path('instituciones/', InstitucionListView.as_view(), name='institucion_list'),
    path('instituciones/<int:pk>/', InstitucionDetailView.as_view(), name='institucion_detail'),
    path('instituciones/add/', InstitucionCreateView.as_view(), name='institucion_add'),
    # ... otras URL
]
