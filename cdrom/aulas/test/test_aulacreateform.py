from django.test import TestCase, Client
from aulas.form import AulaForm
from django.urls import reverse
from django.contrib.auth.models import User
from aulas.models import Aula, CaracteristicaAula


class AulaCreateFormTest(TestCase):
    def setUp(self):
        # Crear algunas características de ejemplo y guardarlas en listas
        self.caracteristica_aire = CaracteristicaAula.objects.create(
            nombre='Aire Acondicionado',
            # disponible=True,
            # se_debe_pedir=False
        )
        self.caracteristica_proyector = CaracteristicaAula.objects.create(
            nombre='Proyector',
            # disponible=False,
            # se_debe_pedir=True
        )

    def test_invalid_capacity(self):
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 0,  # Capacidad inválida (menor o igual a 0)
        }
        form = AulaForm(data=form_data)
        self.assertFalse(form.is_valid())  # Verifica que el formulario sea inválido debido a la capacidad inválida

    def test_valid_form_submission(self):
        aire_id = self.caracteristica_aire.id
        proyector_id = self.caracteristica_proyector.id
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 25,
            'caracteristicas': [aire_id, proyector_id],
        }
        form = AulaForm(data=form_data, files={'foto_aula': None})
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido con datos válidos

    def test_save_form_with_valid_data(self):
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 25,
            'caracteristicas': [self.caracteristica_aire, self.caracteristica_proyector],
        }
        form = AulaForm(data=form_data, files={'foto_aula': None})
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido con datos válidos

        form.save()  # Save the form data to the database

        # Verificar que el objeto Aula fue creado con los datos correctos
        aula = Aula.objects.get(nombre='Aula de Prueba')
        self.assertEqual(aula.nombre, 'Aula de Prueba')
        self.assertEqual(aula.capacidad_alumnos, 25)

    def test_save_form_without_characteristics(self):
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 25,
            'caracteristicas': [],  # No se seleccionan características en este caso
        }
        form = AulaForm(data=form_data, files={'foto_aula': None})
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido con datos válidos

        form.save()  # Save the form data to the database

        # Verificar que el objeto Aula fue creado sin características
        aula = Aula.objects.get(nombre='Aula de Prueba')
        self.assertEqual(aula.nombre, 'Aula de Prueba')
        self.assertEqual(aula.capacidad_alumnos, 25)
        self.assertListEqual(list(aula.caracteristicas.values_list('pk', flat=True)), [])


class AulaCreateViewTest(TestCase):
    def setUp(self):
        # Crear un usuario para usar en las pruebas
        self.client = Client()
        # Crear un usuario comun (no staff)
        self.user = User.objects.create_superuser('juan', 'juan@data99.com.ar', 'juan')
        self.client.raise_request_exception = False

        # URL de la vista de creación del aula
        self.create_url = reverse('aula_add')
        # URL de redirección para usuarios no autenticados
        self.login_url = 'login'

    def test_acceso_a_vista_creacion_sin_autenticar(self):
        # Simula que el usuario no está autenticado
        self.client.logout()

        # Intenta acceder a la vista de creación del aula sin autenticarse
        response = self.client.get(self.create_url)

        # Verifica que el usuario sea redireccionado a la vista de inicio de sesión
        self.assertRedirects(response, self.login_url)

    def test_acceso_a_vista_creacion_autenticado(self):
        # Simula que el usuario está autenticado
        self.client.login(username=self.user.username, password='juan')

        # Intenta acceder a la vista de creación del aula autenticado
        response = self.client.get(self.create_url)

        # Verifica que el usuario tenga acceso a la vista de creación del aula
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aulas/aula_form.html')


    def test_home_for_regular_user(self):
        """ Navegar la home como usuario comun """
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
