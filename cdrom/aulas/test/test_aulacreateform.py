from django.test import TestCase
from aulas.form import AulaCreateForm
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
        form = AulaCreateForm(data=form_data)
        self.assertFalse(form.is_valid())  # Verifica que el formulario sea inválido debido a la capacidad inválida

    def test_valid_form_submission(self):
        aire_id = self.caracteristica_aire.id
        proyector_id = self.caracteristica_proyector.id
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 25,
            'caracteristicas': [aire_id, proyector_id],
        }
        form = AulaCreateForm(data=form_data, files={'foto_aula': None})
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido con datos válidos

    def test_save_form_with_valid_data(self):
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 25,
            'caracteristicas': [self.caracteristica_aire, self.caracteristica_proyector],
        }
        form = AulaCreateForm(data=form_data, files={'foto_aula': None})
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
        form = AulaCreateForm(data=form_data, files={'foto_aula': None})
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido con datos válidos

        form.save()  # Save the form data to the database

        # Verificar que el objeto Aula fue creado sin características
        aula = Aula.objects.get(nombre='Aula de Prueba')
        self.assertEqual(aula.nombre, 'Aula de Prueba')
        self.assertEqual(aula.capacidad_alumnos, 25)
        self.assertListEqual(list(aula.caracteristicas.values_list('pk', flat=True)), [])
