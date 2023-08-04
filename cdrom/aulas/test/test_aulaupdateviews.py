from django.test import TestCase
from django.urls import reverse
from aulas.models import Aula


class AulaUpdateViewTestCase(TestCase):
    def setUp(self):
        # Crea un objeto de ejemplo del modelo Aula para usar en las pruebas
        self.aula = Aula.objects.create(nombre='Aula de prueba', descripcion='Descripción de prueba', capacidad_alumnos=30)
        print(f'Original Aula: {self.aula}')

    def test_actualizar_aula_exitoso(self):
        # Define la URL de la vista de edición del aula con el ID del objeto creado
        url = reverse('aula_edit', args=[self.aula.pk])

        # Datos para actualizar el aula
        data = {
            'nombre': 'Nuevo nombre',
            'descripcion': 'Nueva descripción',
            'capacidad_alumnos': 25,
        }

        # Envía una solicitud POST a la vista para actualizar el aula
        self.client.post(url, data)
        Aula.objects.get(pk=self.aula.pk)

        # Refresca el objeto aula desde la base de datos para obtener los cambios
        self.aula.refresh_from_db()

        # Verifica que los campos del aula se hayan actualizado correctamente
        self.assertEqual(self.aula.nombre, 'Nuevo nombre')
        self.assertEqual(self.aula.descripcion, 'Nueva descripción')
        self.assertEqual(self.aula.capacidad_alumnos, 25)
