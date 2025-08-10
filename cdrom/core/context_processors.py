from django.conf import settings
# from django.urls import reverse
# from core.context_menues import global_menu_context


def app_base_context(request):
    """ Contexto para todos los templates con datos de esta aplicacion """
    return {
        'app_version': settings.APP_VERSION,
        'app_name': settings.APP_NAME,
        'site_brand': settings.APP_LABEL,
        'site_email': settings.APP_EMAIL,
        'site_url': settings.APP_URL,
        # Menues del header
        # 'menues': global_menu_context(),
        }
