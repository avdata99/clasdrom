from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from instituciones.models import Institucion
from instituciones.form import InstitucionForm
User = get_user_model()


class InstitucionListViewTest(TestCase):
    def test_institucion_list_view(self):
        response = self.client.get(reverse('institucion_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instituciones/institucion_list.html')

        institucion = Institucion.objects.create(nombre='Nombre Institucion')

        # Fetch the response again after creating the institucion object
        response = self.client.get(reverse('institucion_list'))

        # Now, check if the institucion name 'Nombre Institucion' is present in the response
        self.assertContains(response, institucion.nombre, count=1, html=False)


class InstitucionDetailViewTest(TestCase):
    def test_institucion_detail_view(self):
        institucion = Institucion.objects.create(nombre='Nombre Institucion')
        response = self.client.get(reverse('institucion_detail', kwargs={'pk': institucion.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instituciones/institucion_detail.html')
        self.assertContains(response, 'Nombre Institucion')


class InstitucionCreateViewTest(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_institucion_create_view(self):
        response = self.client.get(reverse('institucion_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instituciones/institucion_form.html')

        form_data = {
            'nombre': 'Nuevo Nombre',
            # Add more form data if needed
        }
        response = self.client.post(reverse('institucion_add'), data=form_data)

        print("Form is valid:", response.context['form'].is_valid())
        print("Request path:", response.request['PATH_INFO'])
        print("Status code:", response.status_code)
        print("Response content:", response.content.decode('utf-8'))

        self.assertTrue(response.context['form'].is_valid())
        for fs in response.context['formset_fotos']:
            self.assertTrue(fs.is_valid())
        self.assertEqual(response.request['PATH_INFO'], reverse('institucion_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('institucion_list'))

        # Verify that the new institucion is created in the database
        self.assertEqual(Institucion.objects.count(), 1)
        new_institucion = Institucion.objects.first()
        self.assertEqual(new_institucion.nombre, 'Nuevo Nombre')

    def test_institucion_create_view_form_display(self):
        # Obtener la URL para la vista de crear institucion
        url = reverse('institucion_add')

        # Realizar una solicitud GET a la URL
        response = self.client.get(url)

        # Verificar que la respuesta tiene un código de estado 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verificar que el template 'instituciones/institucion_form.html' es utilizado para renderizar la vista
        self.assertTemplateUsed(response, 'instituciones/institucion_form.html')

        # Verificar que el contexto contiene una instancia del formulario InstitucionForm
        self.assertIsInstance(response.context['form'], InstitucionForm)

        # Verificar que el formulario contiene la etiqueta <form>
        self.assertContains(response, '<form')

        # Verificar que el formulario contiene los campos 'Nombre'
        self.assertContains(response, 'Nombre')

        # Verificar que el formulario contiene el botón de submit con la etiqueta 'Guardar'
        self.assertContains(response, 'Guardar')
