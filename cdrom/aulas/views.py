from django.views.generic import DetailView, ListView
from aulas.models import Aula


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
