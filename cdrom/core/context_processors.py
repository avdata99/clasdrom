from django.conf import settings


def app_base_context(request):
    """ Contexto para todos los templates con datos de esta aplicacion """
    return {
        'app_version': settings.APP_VERSION,
        'app_name': settings.APP_NAME,
        'site_brand': settings.APP_LABEL,
        # Menues del header
        'menues': {
            'mact': {
                'titulo': 'Menu activo',
                'active': True,
                'link': 'https://google.com'
            },
            'mcom': {
                'titulo': 'Menu común',
                'link': 'https://google.com'
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
                        'link': 'https://prueba.com'
                    },
                    'm2': {
                        'titulo': '-',
                    },
                    'm3': {
                        'titulo': 'Subitem 2',
                        'link': 'https://lala.com',
                        'disabled': True,
                    }
                }
            }
        }
    }
