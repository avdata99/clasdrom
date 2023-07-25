from django.views.generic import DetailView, ListView
from cursos.models import Curso


class CursoListView(ListView):

    model = Curso
    context_object_name = "cursos"


class CursoDetailView(DetailView):

    model = Curso
    context_object_name = "curso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.nombre
        return context
