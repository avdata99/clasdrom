from django.conf import settings
from django.urls import reverse


def app_base_context(request):
    """ Contexto para todos los templates con datos de esta aplicacion """
    return {
        'app_version': settings.APP_VERSION,
        'app_name': settings.APP_NAME,
        'site_brand': settings.APP_LABEL,
        # Menues del header
        'menues': {
            'mact': {
                'titulo': 'Aulas',
                'active': True,
                'link': reverse('aula_list'),
                'subitems': {
                   'm1': {
                        'titulo': 'Crear Aula',
                        'active': False,
                        'link': reverse('aula_add'),
                    },
                },
            },
            'mcom': {
                'titulo': 'Menu común',
                'link': '#'
            },
            'mdis': {
                'titulo': 'Menu inactivo',
                'disabled': True,
            },
            'mlist': {
                'titulo': 'Lista',
                'link': '#',
                'subitems': {
                    'm1': {
                        'titulo': 'Subitem 1',
                        'link': '#'
                    },
                    'm2': {
                        'titulo': '-',
                    },
                    'm3': {
                        'titulo': 'Subitem 2',
                        'link': '#',
                        'disabled': True,
                    }
                }
            }
        }
    }
