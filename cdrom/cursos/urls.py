from django.urls import path
from cursos.views import (
    CursoDetailView, CursoStaticDetailView,
    CursoListView, CursoStaticPayView,
    CursoStaticPayOKView,
    # , CursoCreateView
)


urlpatterns = [
    path('', CursoListView.as_view(), name='curso_list'),
    path('<slug:slug>/', CursoDetailView.as_view(), name='curso_detail'),
    path('s/<str:curso_name>/', CursoStaticDetailView.as_view(), name='curso_static_detail'),
    path('s/<str:curso_name>-pay/', CursoStaticPayView.as_view(), name='curso_static_pay'),
    path('s/<str:curso_name>-pay-ok/', CursoStaticPayOKView.as_view(), name='curso_static_pay_ok'),
    # path('add/', CursoCreateView.as_view(), name='curso_add'),
]
