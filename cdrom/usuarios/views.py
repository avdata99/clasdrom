import os

from django.views.generic.base import View
from django.views.generic import ListView
from usuarios.mixins import StaffRequiredMixin
from usuarios.enums import UserAction
from usuarios.models import ClasdromUserAction, ClasdromUsuario
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator


class UsersCSVView(StaffRequiredMixin, View):
    """ Devolver un objeto del tipo FileResponse de Django con el archivo que corresponda """
    def get(self, request):
        # Define la ruta completa del archivo a descargar
        file_path = os.path.join(settings.DOWNLOADS_ROOT, 'users.csv')
        if not os.path.exists(file_path):
            # Si el archivo no existe, devuelve una respuesta 404
            return HttpResponse("File not exists", status=404)

        # Abre el archivo y lo devuelve como respuesta de descarga
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=users.csv'
            return response


class UserSystemView(StaffRequiredMixin, ListView):
    """ Vista para ver los detalles de un Usuario del Sistema """
    model = ClasdromUsuario
    context_object_name = 'clasdrom_users'
    template_name = 'users/user_system.html'


class UserActionLoginView(StaffRequiredMixin, ListView):
    """ """
    model = ClasdromUserAction
    context_object_name = 'user_login'
    template_name = 'users/user_login.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(action=UserAction.LOGIN).order_by('-created_at')
        user_filter = self.request.GET.get('user')
        if user_filter:
            self.filtered_user = get_object_or_404(User, username=user_filter)
            queryset = queryset.filter(clasdrom_user__user=self.filtered_user)
        else:
            self.filtered_user = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['filtered_user'] = self.filtered_user
        # Obtener el número de página actual
        page = self.request.GET.get('page')

        # Crear un objeto Paginator y especificar el número de elementos por página
        paginator = Paginator(context['user_login'], 100)  # Mostrar 10 elementos por página

        # Obtener la página solicitada del paginador
        user_login = paginator.get_page(page)

        # Agregar el objeto de paginación al contexto
        context['user_login'] = user_login

        return context
