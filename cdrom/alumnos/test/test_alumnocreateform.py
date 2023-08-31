from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from alumnos.models import Alumno
from alumnos.forms import AlumnoForm


class AlumnoCreateFormTest(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_superuser('juan', 'juan@data99.com.ar', 'juan')

    def test_valid_form_submission(self):
        form_data = {
            'nombres': 'Juan',
            'apellidos': 'Perez',
            'persona_id': '37234584',  # Replace with a valid ID
            'celular_principal': None,
            'email_principal': 'juan@example.com',
            'site': 1,
        }
        form = AlumnoForm(data=form_data)
        print(form.errors)  # Print form errors
        self.assertTrue(form.is_valid())  # Verifies that the form is valid with valid data

    def test_save_form_with_valid_data(self):
        form_data = {
            'nombres': 'Juan',
            'apellidos': 'Perez',
            'persona_id': '12345678',
            'celular_principal': None,
            'email_principal': 'juan@example.com',
            'matricula_id': 1,
            'site': 'www.sitio.com',
        }
        form = AlumnoForm(data=form_data)
        print(form.errors)  # Print form errors
        self.assertTrue(form.is_valid())  # Verifies that the form is valid with valid data

        form.save()  # Save the form data to the database

        # Verify that the Alumno object was created with the correct data
        alumno = Alumno.objects.get(nombres='Juan', apellidos='Perez')
        self.assertEqual(alumno.nombres, 'Juan')
        self.assertEqual(alumno.apellidos, 'Perez')

    def test_save_form_without_required_fields(self):
        form_data = {
            'nombres': '',
            'apellidos': 'Perez',
            'persona_id': '12345678',
            'celular_principal': None,
            'email_principal': 'juan@example.com',
        }
        form = AlumnoForm(data=form_data)
        print(form.errors)  # Print form errors
        self.assertFalse(form.is_valid())  # Verifies that the form is invalid due to missing data
        self.assertIn('nombres', form.errors)  # Verifies that 'nombres' field has errors


class AlumnoCreateViewTest(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_superuser('juan', 'juan@data99.com.ar', 'juan')

        # URL of the alumno creation view
        self.create_url = reverse('alumno_add')

    def test_access_to_creation_view_unauthenticated(self):
        # Try to access the alumno creation view without authenticating
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))
        # Verifies that the user is redirected to the login view

    def test_access_to_creation_view_authenticated(self):
        # Simulate that the user is authenticated
        self.client.login(username=self.user.username, password='juan')

        # Try to access the alumno creation view while authenticated
        response = self.client.get(self.create_url)

        # Verifies that the user has access to the alumno creation view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alumnos/alumno_form.html')
