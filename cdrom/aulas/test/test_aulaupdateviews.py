from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from aulas.models import Aula, CaracteristicaEnAula, FotoAula, CaracteristicaAula
from aulas.form import AulaForm


class AulaUpdateViewTestCase(TestCase):
    def setUp(self):
        # Crea un objeto de ejemplo del modelo Aula para usar en las pruebas
        self.aula = Aula.objects.create(nombre='Aula de prueba', descripcion='Descripción de prueba', capacidad_alumnos=30)
        self.caracteristica = CaracteristicaAula.objects.create(nombre='AC')
        CaracteristicaEnAula.objects.create(aula=self.aula, caracteristica=self.caracteristica)
        # Crea una foto asociada al aula
        self.foto = FotoAula.objects.create(aula=self.aula, foto='', orden=1)
        print(f'Original Aula: {vars(self.aula)}')

    def test_actualizar_aula_exitoso(self):
        # Define la URL de la vista de edición del aula con el ID del objeto creado
        url = reverse('aula_edit', args=[self.aula.pk])
        dummy_image = SimpleUploadedFile("dummy_image.png", b"file_content", content_type="image/png")

        # Datos para actualizar el aula
        data = {
                'nombre': 'Nuevo nombre',
                'descripcion': 'Nueva descripción',
                'capacidad_alumnos': 25,
                'caracteristicas-TOTAL_FORMS': 2,
                'caracteristicas-INITIAL_FORMS': 1,
                'caracteristicas-MIN_NUM_FORMS': 0,
                'caracteristicas-MAX_NUM_FORMS': 1000,
                'caracteristicas-0-caracteristica': 2,
                'caracteristicas-0-disponible': 'on',
                'caracteristicas-0-id': 2,
                'caracteristicas-0-aula': 1,
                'caracteristicas-1-caracteristica': 1,
                'caracteristicas-1-disponible': 'on',
                'fotos-TOTAL_FORMS': 2,
                'fotos-INITIAL_FORMS': 1,
                'fotos-MIN_NUM_FORMS': 0,
                'fotos-MAX_NUM_FORMS': 1000,
                'fotos-0-foto': dummy_image,
                'fotos-0-orden': 100,
                'fotos-0-descripcion': 'descripcion',
                'fotos-0-id': 7,
                'fotos-0-aula': 1,
                'fotos-1-foto': '(binary)',
                'fotos-1-orden': 100,
                'fotos-1-descripcion': '',
                'fotos-1-id': 10,
                'fotos-1-aula': 7,
            }

        # Envía una solicitud POST a la vista para actualizar el aula
        response = self.client.post(url, data)
        print(f'Solicitud POST enviada: {data}')

        # Verifique que la respuesta tenga un código de estado exitoso (por ejemplo, 200 OK)
        self.assertEqual(response.status_code, 200)

        # Refresca el objeto aula desde la base de datos para obtener los cambios
        aula = Aula.objects.get(nombre='Nuevo nombre')

        # Verifica que los campos del aula se hayan actualizado correctamente
        self.assertEqual(aula.descripcion, 'Nueva descripción')
        self.assertEqual(aula.capacidad_alumnos, 25)

        # Assert that caracteristicas_formset data is saved correctly
        caracteristicas = CaracteristicaEnAula.objects.filter(aula=aula)
        self.assertEqual(caracteristicas.count(), 1)  # Adjust count based on your data

        # Assert that fotos_formset data is saved correctly
        fotos = FotoAula.objects.filter(aula=aula)
        self.assertEqual(fotos.count(), 1)  # Adjust count based on your data

    def test_aula_update_view(self):
        # Obtiene la URL para acceder a la vista de edición del aula con el ID del objeto creado
        url = reverse('aula_edit', args=[self.aula.pk])
        # Realiza una solicitud GET a la vista para obtener la respuesta
        response = self.client.get(url)

        # Verifica que la respuesta tenga un código de estado exitoso (por ejemplo, 200 OK)
        self.assertEqual(response.status_code, 200)

        # Verifica que se esté utilizando la plantilla correcta
        self.assertTemplateUsed(response, 'aulas/aula_edit.html')

        # Verifica que el formulario en el contexto sea una instancia de AulaForm
        form = response.context['form']
        self.assertIsInstance(form, AulaForm)
