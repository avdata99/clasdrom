from django.views.generic import DetailView, ListView
from aulas.models import Aula


class AulaListView(ListView):

    model = Aula
    context_object_name = "aulas"


class AulaDetailView(DetailView):

    model = Aula
    context_object_name = "aula"
