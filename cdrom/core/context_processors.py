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
                'titulo': 'Cursos',
                'active': True,
                'subitems': {
                    'm1': {
                        'titulo': 'Listar Cursos',
                        'active': False,
                        'link': reverse('curso_list'),
                    },
                    'm2': {
                        'titulo': '-',
                    },
                    'm3': {
                        'titulo': 'Crear Curso',
                        'active': False,
                        'link': reverse('curso_add'),
                    },
                },
            },

            'mlist2': {
                'titulo': 'Instituciones',
                'active': True,
                'subitems': {
                    'm1': {
                        'titulo': 'Listar Instituciones',
                        'active': False,
                        'link': reverse('institucion_list'),
                    },
                    'm2': {
                        'titulo': '-',
                    },
                    'm3': {
                        'titulo': 'Crear Institucion',
                        'active': False,
                        'link': reverse('institucion_add'),
                    }
                }
            }
        }
    }
