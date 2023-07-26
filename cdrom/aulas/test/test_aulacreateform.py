from django.test import TestCase
from aulas.form import AulaCreateForm
from aulas.models import CaracteristicaAula


class AulaCreateFormTest(TestCase):
    def setUp(self):
        # Crear algunas características de ejemplo
        CaracteristicaAula.objects.create(nombre='Aire Acondicionado', disponible=True, se_debe_pedir=False)
        CaracteristicaAula.objects.create(nombre='Proyector', disponible=False, se_debe_pedir=True)

    def test_invalid_capacity(self):
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 0,  # Capacidad inválida (menor o igual a 0)
        }
        form = AulaCreateForm(data=form_data)
        self.assertFalse(form.is_valid())  # Verifica que el formulario sea inválido debido a la capacidad inválida

    def test_valid_form_submission(self):
        form_data = {
            'nombre': 'Aula de Prueba',
            'capacidad_alumnos': 25,
            'caracteristicas': [1, 2],  # IDs de las características creadas en setUp
        }
        form = AulaCreateForm(data=form_data, files={'foto_aula': None})
        self.assertTrue(form.is_valid())  # Verifica que el formulario sea válido con datos válidos
