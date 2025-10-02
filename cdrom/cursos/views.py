from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.http import Http404
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from cursos.models import Curso
from django.urls import reverse_lazy
from cursos.form import CursoForm


class CursoListView(ListView):

    model = Curso
    context_object_name = "lista"


class CursoDetailView(DetailView):

    model = Curso
    context_object_name = "curso"
    template_name = "cursos/curso_detail.html"
    slug_field = "code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_brand'] = self.object.titulo
        return context


class CursoStaticDetailView(TemplateView):
    """ This is a static site for a course.
    We have the kwarg 'curso_name' to identify the course to define the template.
    """

    def get_template_names(self):
        curso_name = self.kwargs.get('curso_name')
        if not curso_name:
            raise Http404("Curso no definido")

        # Check if the template exists using a simpler approach
        template = f'cursos/s/{curso_name}.html'
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise Http404("Curso no encontrado")

        return [template]


class CursoStaticPayView(TemplateView):
    """ This is a static pay site for a course.
    We have the kwarg 'curso_name' to identify the course to define the template.
    """

    def get_template_names(self):
        curso_name = self.kwargs.get('curso_name')
        if not curso_name:
            raise Http404("Curso no definido")

        # Check if the template exists using a simpler approach
        template = f'cursos/s/{curso_name}-pay.html'
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise Http404("Curso no encontrado")

        return [template]


class CursoStaticPayOKView(TemplateView):
    """ This is a static pay thank you site for a course.
    We have the kwarg 'curso_name' to identify the course to define the template.
    """

    def get_template_names(self):
        curso_name = self.kwargs.get('curso_name')
        if not curso_name:
            raise Http404("Curso no definido")

        # Check if the template exists using a simpler approach
        template = f'cursos/s/{curso_name}-pay-ok.html'
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise Http404("Curso no encontrado")

        return [template]


class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    success_url = reverse_lazy('curso_list')
