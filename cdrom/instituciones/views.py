import logging
from django.views.generic import DetailView, ListView, CreateView
from .models import Institucion
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import InstitucionForm, FotoInstitucionFormSet


logger = logging.getLogger(__name__)


class InstitucionListView(ListView):
    model = Institucion
    context_object_name = "lista"


class InstitucionDetailView(DetailView):
    model = Institucion
    context_object_name = "institucion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.nombre
        return context


class InstitucionCreateView(LoginRequiredMixin, CreateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'instituciones/institucion_form.html'
    success_url = reverse_lazy('institucion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # FormSets
        context['formset_fotos'] = FotoInstitucionFormSet(
            self.request.POST or None, self.request.FILES or None, instance=self.object
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_fotos = context['formset_fotos']
        formset_instituciones = context['formset_instituciones']

        if formset_fotos.is_valid() and formset_instituciones.is_valid():
            self.object = form.save()
            formset_fotos.instance = self.object
            formset_fotos.save()
            formset_instituciones.instance = self.object
            formset_instituciones.save()
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))
