from django.conf import settings
from django.urls import reverse


def app_base_context(request):
    """ Contexto para todos los templates con datos de esta aplicacion """
    menues = {
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
                    },
                },
            },

            'mlist3': {
                'titulo': 'Account',
                'link': '#',
                'subitems': {
                    'm1': {
                        'titulo': 'Logout',
                        'link': reverse('logout')
                    },
                    'm2': {
                        'titulo': '-',
                    },
                    'm3': {
                        'titulo': 'My Settings',
                        'link': reverse('my-settings'),
                        # 'disabled': True,
                    },
                }
            }
        }
    }

    if request.user.is_staff:
        admin = {
            'titulo': 'Staff',
            'link': '#',
            'subitems': {
                'admin': {
                    'titulo': 'Admin',
                    'link': reverse('admin:index'),
                },
                'sep': {'titulo': '-'},
                'users': {
                    'titulo': 'Users',
                    'link': '#',
                    'disabled': True,
                },
                'user_login': {
                    'titulo': 'User Login',
                    'link': reverse('users-login'),
                },
                'user_system': {
                    'titulo': 'App users',
                    'link': reverse('users-system'),
                },

            }
        }

        menues['menues']['admin'] = admin
    return menues
