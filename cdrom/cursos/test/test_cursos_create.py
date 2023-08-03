from django.test import TestCase
from django.urls import reverse
from cursos.models import Curso
from cursos.form import CursoForm


class CursoListViewTest(TestCase):
    def test_curso_list_view(self):
        response = self.client.get(reverse('curso_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/curso_list.html')

        curso = Curso.objects.create(titulo='Curso 1')

        # Fetch the response again after creating the curso object
        response = self.client.get(reverse('curso_list'))

        # Now, check if the curso title 'Curso 1' is present in the response
        self.assertContains(response, curso.titulo, count=1, html=False)


class CursoDetailViewTest(TestCase):
    def test_curso_detail_view(self):
        curso = Curso.objects.create(titulo='Curso 1', descripcion='This is a curso.')
        response = self.client.get(reverse('curso_detail', kwargs={'pk': curso.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/curso_detail.html')
        self.assertContains(response, 'Curso 1')
        self.assertContains(response, 'This is a curso.')


class CursoCreateViewTest(TestCase):
    def test_curso_create_view(self):
        response = self.client.get(reverse('curso_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/curso_form.html')

        # Test form submission
        form_data = {
            'titulo': 'New Curso',
            'descripcion': 'This is a new curso.',
        }
        response = self.client.post(reverse('curso_add'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after form submission
        self.assertRedirects(response, reverse('curso_list'))  # Should redirect to curso_list view

        # Verify that the new curso is created in the database
        self.assertEqual(Curso.objects.count(), 1)
        new_curso = Curso.objects.first()
        self.assertEqual(new_curso.titulo, 'New Curso')
        self.assertEqual(new_curso.descripcion, 'This is a new curso.')

    def test_curso_create_view_form_display(self):
        # Obtener la URL para la vista de crear curso
        url = reverse('curso_add')

        # Realizar una solicitud GET a la URL
        response = self.client.get(url)

        # Verificar que la respuesta tiene un código de estado 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verificar que el template 'cursos/curso_form.html' es utilizado para renderizar la vista
        self.assertTemplateUsed(response, 'cursos/curso_form.html')

        # Verificar que el contexto contiene una instancia del formulario CursoForm
        self.assertIsInstance(response.context['form'], CursoForm)

        # Verificar que el formulario contiene la etiqueta <form>
        self.assertContains(response, '<form')

        # Verificar que el formulario contiene los campos 'Institucion', 'Titulo' y 'Descripcion'
        self.assertContains(response, 'Institucion')
        self.assertContains(response, 'Titulo')
        self.assertContains(response, 'Descripcion')

        # Verificar que el formulario contiene el botón de submit con la etiqueta 'Crear'
        self.assertContains(response, 'Guardar')
