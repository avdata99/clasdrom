from django.views.generic import DetailView, ListView, CreateView
from aulas.models import Aula
from django.urls import reverse_lazy
from aulas.form import AulaForm, AulasFeaturesFormSet


class AulaListView(ListView):

    model = Aula
    context_object_name = "aulas"


class AulaDetailView(DetailView):

    model = Aula
    context_object_name = "aula"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.nombre
        # Obtener las fotos asociadas al aula
        context["fotos"] = self.object.fotos.all()
        return context


class AulaCreateView(CreateView):
    model = Aula
    template_name = 'aulas/aula_form.html'
    success_url = reverse_lazy('aula_list')
    form_class = AulaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AulasFeaturesFormSet(self.request.POST)
        else:
            context['formset'] = AulasFeaturesFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
