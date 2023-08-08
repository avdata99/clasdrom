from django.test import TestCase
from django.urls import reverse
from aulas.models import Aula, CaracteristicaEnAula, FotoAula
from aulas.form import AulaForm


class AulaUpdateViewTestCase(TestCase):
    def setUp(self):
        # Crea un objeto de ejemplo del modelo Aula para usar en las pruebas
        self.aula = Aula.objects.create(nombre='Aula de prueba', descripcion='Descripción de prueba', capacidad_alumnos=30)
        print(f'Original Aula: {vars(self.aula)}')

    def test_actualizar_aula_exitoso(self):
        # Define la URL de la vista de edición del aula con el ID del objeto creado
        url = reverse('aula_edit', args=[self.aula.pk])

        # Datos para actualizar el aula
        data = {
            'nombre': 'Nuevo nombre',
            'descripcion': 'Nueva descripción',
            'capacidad_alumnos': 25,
            'form-0-caracteristica': '',
        }
        # Agregar datos de formset al diccionario de datos
        caracteristicas_formset_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-caracteristica': '1',  # Ejemplo de valor para caracteristica
            'form-0-disponible': 'True',   # Ejemplo de valor para disponible
        }

        fotos_formset_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-foto': '',  # Ejemplo de valor para foto
            'form-0-orden': '1',  # Ejemplo de valor para for orden
        }

        data.update(caracteristicas_formset_data)
        data.update(fotos_formset_data)

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
