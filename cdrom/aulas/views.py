import logging
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from aulas.form import AulaForm, AulasFeaturesFormSet, FotoAulasFormSet
from aulas.models import Aula


logger = logging.getLogger(__name__)


class AulaListView(ListView):

    model = Aula
    context_object_name = "aulas"


class AulaDetailView(LoginRequiredMixin, DetailView):

    model = Aula
    context_object_name = "aula"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.nombre
        # Obtener las fotos asociadas al aula
        context["fotos"] = self.object.fotos.all()
        return context


class AulaCreateView(LoginRequiredMixin, CreateView):
    model = Aula
    template_name = 'aulas/aula_form.html'
    success_url = reverse_lazy('aula_list')
    form_class = AulaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            logger.info(f'Aula creation\n\t{self.request.POST}\n\t{self.request.FILES}')
            context['formset'] = AulasFeaturesFormSet(self.request.POST)
            context['formset_fotos'] = FotoAulasFormSet(self.request.POST, self.request.FILES)

        else:
            context['formset'] = AulasFeaturesFormSet()
            context['formset_fotos'] = FotoAulasFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        formset_fotos = context['formset_fotos']

        if formset.is_valid() and formset_fotos.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            formset_fotos.instance = self.object
            formset_fotos.save()
        else:
            return super().form_invalid(form)

        return super().form_valid(form)


class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aulas/aula_edit.html'  # Especifica la ruta del template de edición

    def get_success_url(self):
        # Redireccionar a la vista de detalle del aula con el ID del aula actual
        return reverse_lazy('aula_detail', args=[self.object.pk])
