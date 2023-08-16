import os
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from aulas.models import Aula, CaracteristicaEnAula, FotoAula, CaracteristicaAula
from aulas.form import AulaForm


class AulaUpdateViewTestCase(TestCase):
    def setUp(self):
        # Crea un objeto de ejemplo del modelo Aula para usar en las pruebas
        self.aula = Aula.objects.create(nombre='Aula de prueba', descripcion='Descripción de prueba', capacidad_alumnos=30)
        self.caracteristica = CaracteristicaAula.objects.create(nombre='AC-calor')
        CaracteristicaEnAula.objects.create(aula=self.aula, caracteristica=self.caracteristica)
        print(f'"Initial Aula before update:" {vars(self.aula)}')

    def test_actualizar_aula_exitoso(self):
        # Define la URL de la vista de edición del aula con el ID del objeto creado
        url = reverse('aula_edit', args=[self.aula.pk])
        # Ruta absoluta al archivo logo.png en tu sistema de archivos
        archivo1_ruta = os.path.join('aulas/test/file_test', 'imagen.png')
        archivo2_ruta = os.path.join('aulas/test/file_test', 'imagen.png')
        if not os.path.exists(archivo1_ruta) or not os.path.exists(archivo2_ruta):
            raise Exception('Imagen not exists')

        # Abrir y cargar el archivo desde la ubicación
        archivo1 = open(archivo1_ruta, 'rb')
        content1 = archivo1.read()  # Leer el contenido del archivo
        archivo1_subida = SimpleUploadedFile(
            name='imagen.png',
            content=content1,
            content_type='image/png',
        )
        archivo2 = open(archivo2_ruta, 'rb')
        content2 = archivo2.read()  # Leer el contenido del archivo
        archivo2_subida = SimpleUploadedFile(
            name='imagen.png',
            content=content2,
            content_type='image/png',
        )

        # Datos para actualizar el aula
        data = {
                'csrfmiddlewaretoken': 'BFbthUbu1Uajxua5m2B7ToUhtd8dNO220PbY7WsqGbTxyE69G0N6cIWqOATEyg9n',
                'institucion': '1',
                'nombre': 'Nuevo nombre',
                'descripcion': 'Nueva descripción',
                'capacidad_alumnos': 25,
                'caracteristicas-TOTAL_FORMS': 2,
                'caracteristicas-INITIAL_FORMS': 1,
                'caracteristicas-MIN_NUM_FORMS': 0,
                'caracteristicas-MAX_NUM_FORMS': 1000,
                'caracteristicas-0-caracteristica': 1,
                'caracteristicas-0-disponible': True,
                'caracteristicas-0-id': 1,
                'caracteristicas-0-aula': 1,
                'caracteristicas-1-caracteristica': '',
                'caracteristicas-1-disponible': True,
                'caracteristicas-1-id': '',
                'caracteristicas-1-aula': 1,
                'fotos-TOTAL_FORMS': 2,
                'fotos-INITIAL_FORMS': 1,
                'fotos-MIN_NUM_FORMS': 0,
                'fotos-MAX_NUM_FORMS': 1000,
                'fotos-0-foto': archivo1_subida,
                'fotos-0-orden': 100,
                'fotos-0-descripcion': '',
                'fotos-0-id': 1,
                'fotos-0-aula': 1,
                'fotos-1-foto': archivo2_subida,
                'fotos-1-orden': 100,
                'fotos-1-descripcion': '',
                'fotos-1-id': 2,
                'fotos-1-aula': 1,
            }

        # Envía una solicitud POST a la vista para actualizar el aula
        response = self.client.post(
            path=url,
            data=data,
            follow=True,
        )
        print(f'Solicitud POST enviada: {data}')
        print("Actual URL:", response.request['PATH_INFO'])
        print("Response status code:", response.status_code)

        try:
            expected_url = reverse('aula_detail', args=[self.aula.pk])
            print("Expected URL:", expected_url)
            self.assertEqual(response.request['PATH_INFO'], expected_url)
            # Verifique que la respuesta tenga un código de estado exitoso (por ejemplo, 200 OK)
            self.assertEqual(response.status_code, 200)
            print("status code", response.status_code)
            # Refresca el objeto aula desde la base de datos antes de la actualización
            self.aula.refresh_from_db()

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
            # Print the state of the Aula after the update
            aula.refresh_from_db()
            updated_aula = Aula.objects.get(nombre='Nuevo nombre')
            print("Updated Aula:", vars(updated_aula))
        except AssertionError as e:
            print("Error en el test:", e)
            raise e  # Vuelve a lanzar la excepción para que el test falle correctamente

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


# este es el payload que debe generar.

"""
csrfmiddlewaretoken: BFbthUbu1Uajxua5m2B7ToUhtd8dNO220PbY7WsqGbTxyE69G0N6cIWqOATEyg9n
institucion: 1
nombre: Nuevo nombre
descripcion: Nueva descripción
capacidad_alumnos: 25
caracteristicas-TOTAL_FORMS: 2
caracteristicas-INITIAL_FORMS: 1
caracteristicas-MIN_NUM_FORMS: 0
caracteristicas-MAX_NUM_FORMS: 1000
caracteristicas-0-caracteristica: 1
caracteristicas-0-disponible: on
caracteristicas-0-id: 1
caracteristicas-0-aula: 1
caracteristicas-1-caracteristica:
caracteristicas-1-disponible: on
caracteristicas-1-id:
caracteristicas-1-aula: 1
fotos-TOTAL_FORMS: 2
fotos-INITIAL_FORMS: 1
fotos-MIN_NUM_FORMS: 0
fotos-MAX_NUM_FORMS: 1000
fotos-0-foto: (binary)
fotos-0-orden: 100
fotos-0-descripcion:
fotos-0-id: 1
fotos-0-aula: 1
fotos-1-foto: (binary)
fotos-1-orden: 100
fotos-1-descripcion:
fotos-1-id:
fotos-1-aula: 1
"""
