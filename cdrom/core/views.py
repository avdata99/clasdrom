from django.shortcuts import render
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
