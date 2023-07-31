from django.views.generic import DetailView, ListView, CreateView
from cursos.models import Curso
from django.urls import reverse_lazy
from cursos.form import CursoForm


class CursoListView(ListView):

    model = Curso
    context_object_name = "cursos"


class CursoDetailView(DetailView):

    model = Curso
    context_object_name = "curso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.titulo
        return context


class CursoCreateView(CreateView):
    model = Curso
    # fields = ['institucion', 'nombre', 'descripcion', 'capacidad_alumnos']
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    success_url = reverse_lazy('curso_list')
