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
                'subitems': {
                   'm1': {
                        'titulo': 'Listar Aulas',
                        'active': False,
                        'link': reverse('aula_list'),
                    },
                   'm2': {
                        'titulo': 'Crear Aula',
                        'active': False,
                        'link': reverse('aula_add'),
                    },
                },
            },
            'mcom': {
                'titulo': 'Profesores',
                'active': True,
                'subitems': {
                   'm1': {
                        'titulo': 'Listar Profesores',
                        'active': False,
                        'link': reverse('profe_list'),
                    },
                   'm2': {
                        'titulo': 'Cargar profesor',
                        'active': False,
                        'link': reverse('profe_add'),
                    },
                },
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
