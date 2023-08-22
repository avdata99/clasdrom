from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginPageView(TemplateView):
    """ Vista del login del sitio """
    template_name = 'login-page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = 'Login | Clasdrom'
        context['login_post_url'] = reverse('admin:login')
        context['google_client_id'] = settings.GOOGLE_CLIENT_ID
        context['redirect_uri'] = f'{settings.APP_PROTOCOL}://{settings.APP_DOMAIN}/{settings.GOOGLE_REDIRECT_URI}/'
        return context


class MySettingsView(LoginRequiredMixin, TemplateView):
    """ Vista del usuario """
    template_name = 'my-settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = 'My Settings'
        return context
