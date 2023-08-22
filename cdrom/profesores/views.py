import logging
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from profesores.forms import ProfesorForm
from profesores.models import Profesor


logger = logging.getLogger(__name__)


class ProfesorListView(ListView):
    """vista para mostrar la lista de profesores del sistema"""
    model = Profesor
    context_object_name = "profesores"
    template_name = "profe/profe_list.html"


class ProfesorDetailView(LoginRequiredMixin, DetailView):
    """Vista para mostrar los detalles de un profesor en el sistema"""
    model = Profesor
    context_object_name = "profesor"
    template_name = "profe/profe_detail.html"


class ProfesorCreateView(LoginRequiredMixin, CreateView):
    """vista apra crear un nuevo Profesor en el sistema"""
    model = Profesor
    template_name = 'profe/profe_form.html'
    success_url = reverse_lazy('profe_list')
    form_class = ProfesorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            logger.info(f'Profesor creation\n\t{self.request.POST}')
        return context

    def form_valid(self, form):
        return super().form_valid(form)
