import os
import tempfile
import shutil
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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

        # Create a temporary media root for testing
        self.temp_media_root = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary files
        if hasattr(self, 'temp_media_root') and os.path.exists(self.temp_media_root):
            shutil.rmtree(self.temp_media_root)

    def test_institucion_create_view(self):
        response = self.client.get(reverse('institucion_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instituciones/institucion_form.html')

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_institucion_create_add_ok(self):
        # Ruta absoluta al archivo logo.png en tu sistema de archivos
        archivo1_ruta = os.path.join('instituciones/test/file_test', 'logo.png')
        archivo2_ruta = os.path.join('instituciones/test/file_test', 'logo.png')
        if not os.path.exists(archivo1_ruta) or not os.path.exists(archivo2_ruta):
            raise Exception('Logo not exists')

        # Abrir y cargar el archivo desde la ubicación
        with open(archivo1_ruta, 'rb') as archivo1:
            content1 = archivo1.read()
            archivo1_subida = SimpleUploadedFile(
                name='logo.png',
                content=content1,
                content_type='image/png',
            )

        with open(archivo2_ruta, 'rb') as archivo2:
            content2 = archivo2.read()
            archivo2_subida = SimpleUploadedFile(
                name='logo2.png',
                content=content2,
                content_type='image/png',
            )

        form_data = {
            'nombre': 'Nuevo Nombre',
            'logo': archivo1_subida,  # Agregar el archivo de subida al formulario
            'fotos-TOTAL_FORMS': '1',
            'fotos-INITIAL_FORMS': '0',
            'fotos-MIN_NUM_FORMS': '0',
            'fotos-MAX_NUM_FORMS': '1000',
            'fotos-0-foto': archivo2_subida,  # Agregar la foto al formset de fotos'
            'fotos-0-orden': 1,  # Agregar otros campos del formset si es necesario
            'fotos-0-descripcion': 'Descripción de la foto',
            # Agregar más datos de formulario si es necesario
        }

        response = self.client.post(
            reverse('institucion_add'),
            form_data,
            follow=True,
        )

        self.assertEqual(response.request['PATH_INFO'], reverse('institucion_list'))
        self.assertEqual(response.status_code, 200)
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
