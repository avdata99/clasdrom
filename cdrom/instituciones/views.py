import logging
from django.views.generic import DetailView, ListView, CreateView
from .models import Institucion
from django.urls import reverse
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
    # prefiero una funcion success_url = reverse_lazy('institucion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("contex 001", context)
        if self.request.POST:
            context['form'] = InstitucionForm(self.request.POST, self.request.FILES)
            print("context1 002 ", context, self.request.POST, self.request.FILES)
            context['formset_fotos'] = FotoInstitucionFormSet(self.request.POST, self.request.FILES)
            print("context2 003", context, self.request.POST, self.request.FILES)

        else:
            context['form'] = InstitucionForm()
            print("context1 004:", context)
            context['formset_fotos'] = FotoInstitucionFormSet()
            print("context2 005:", context)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        print("context from valid:", context)
        formset_fotos = context['formset_fotos']
        print("Form is valid 006:", form.is_valid())
        print("Formset is valid 007:", formset_fotos.is_valid())

        if form.is_valid() and formset_fotos.is_valid():
            self.object = form.save()
            print("Form saved 008")
            self.object.site = Site.objects.get_current()
            formset_fotos.instance = self.object
            formset_fotos.save()
            print("Formset saved 009")
            return super().form_valid(form)
        else:
            print("Form errors 010:", form.errors)
            print("Formset errors 011", formset_fotos.errors)
            return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        success_url = reverse('institucion_list')
        print(f'Redirect to {success_url}')
        return success_url
