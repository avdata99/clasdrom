import logging
from django.urls import reverse
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

    def get_success_url(self, **kwargs):
        success_url = reverse('aula_list')
        return success_url


class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aulas/aula_edit.html'  # Especifica la ruta del template de edición

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("contex 000", context)
        if self.request.POST:
            logger.info(f'Aula update\n\t{self.request.POST}\n\t{self.request.FILES}')
            context['caracteristicas_formset'] = AulasFeaturesFormSet(self.request.POST, instance=self.object)
            print(f'context 001: {context}')
            context['fotos_formset'] = FotoAulasFormSet(self.request.POST, self.request.FILES, instance=self.object)
            print(f'context 002: {context}')

        else:
            context['fotos_formset'] = FotoAulasFormSet(instance=self.object)
            print(f'context 003: {context}')
            context['caracteristicas_formset'] = AulasFeaturesFormSet(instance=self.object)
            print(f'context 004: {context}')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        print("context from valid 005:", context)
        caracteristicas_formset = context['caracteristicas_formset']
        print("Form is valid 006:", form.is_valid())
        fotos_formset = context['fotos_formset']
        print("Formset is valid 007:", fotos_formset.is_valid())

        # Imprimir el contenido del payload
        print("Payload data:", self.request.POST)

        c_valid = caracteristicas_formset.is_valid()
        f_valid = fotos_formset.is_valid()
        logger.info(f'c valid {c_valid}')
        logger.info(f'f valid {f_valid}')
        print(f'c_valid:{c_valid}')
        print(f'f_valid:{f_valid}')
        if c_valid and f_valid:
            self.object = form.save()
            print("Form saved 008")
            caracteristicas_formset.instance = self.object
            caracteristicas_formset.save()
            fotos_formset.instance = self.object
            fotos_formset.save()
            print("Formset saved 009")
            return super().form_valid(form)
        else:
            print("Form errors 010:", form.errors)
            print("Formset errors 011", fotos_formset.errors)
            return super().form_invalid(form)


    def get_success_url(self):
        # Redireccionar a la vista de detalle del aula con el ID del aula actual
        success_url = reverse('aula_detail', args=[self.object.pk])
        print("Generated success URL:", success_url)
        return success_url
