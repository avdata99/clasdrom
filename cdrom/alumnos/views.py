from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from alumnos.models import Alumno
from .forms import AlumnoForm


class AlumnoListView(ListView):
    model = Alumno
    # template_name = 'alumnos/alumno_list.html'
    context_object_name = 'alumnos'


class AlumnoCreateView(LoginRequiredMixin, CreateView):
    template_name = 'alumnos/alumno_form.html'

    def get(self, request):
        form = AlumnoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save()
            return redirect('alumno_detail', pk=alumno.pk)  # Replace 'alumno_detail' with your detail view name
        return render(request, self.template_name, {'form': form})


class AlumnoDetailView(DetailView):
    model = Alumno
    context_object_name = 'alumno'
    template_name = 'alumnos/alumno_detail.html'
