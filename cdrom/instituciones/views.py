import logging
from django.views.generic import DetailView, ListView, CreateView
from .models import Institucion
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
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
        if self.request.POST:
            context['form'] = InstitucionForm(self.request.POST, self.request.FILES)
            context['formset_fotos'] = FotoInstitucionFormSet(self.request.POST, self.request.FILES)

        else:
            context['form'] = InstitucionForm()
            context['formset_fotos'] = FotoInstitucionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_fotos = context['formset_fotos']
        print("Form is valid:", form.is_valid())
        print("Formset is valid:", formset_fotos.is_valid())    

        if form.is_valid() and formset_fotos.is_valid():
            self.object = form.save()
            print("Form saved")
            self.object.site = Site.objects.get_current()
            formset_fotos.instance = self.object
            formset_fotos.save()
            print("Formset saved")
        else:
            print("Form is invalid:", form.errors)
            print("Formset is invalid:", formset_fotos.errors)
            return super().form_invalid(form)

        return super().form_valid(form)
