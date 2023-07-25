from django.views.generic import DetailView, ListView, CreateView
from aulas.models import Aula
from django.urls import reverse_lazy
from aulas.form import AulaCreateForm


class AulaListView(ListView):

    model = Aula
    context_object_name = "aulas"


class AulaDetailView(DetailView):

    model = Aula
    context_object_name = "aula"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.nombre
        return context


class AulaCreateView(CreateView):
    model = Aula
    # fields = ['institucion', 'nombre', 'descripcion', 'capacidad_alumnos']
    form_class = AulaCreateForm
    template_name = 'aulas/aula_form.html'
    success_url = reverse_lazy('aula_list')
