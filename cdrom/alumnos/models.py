from django.db import models
from alumnos.helpers import generar_matricula_id, generar_pre_inscripcion_id
from core.models import Persona
from cursos.models import Curso


class PreInscripcion(models.Model):
    """ Primera instancia generica donde tomamos datos sin mucha validacion
        Esto es para el formulario de pre-inscripcion y va a requerir trabajo
        para procesarlo, conversar con un interesado y convencerlo de que se inscriba.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    # Le vamos a dar un codigo único a cada preinscripto
    code = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'PreInscripcion {self.nombre}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_pre_inscripcion_id(self.curso)
        super().save(*args, **kwargs)


class PreInscripcionExtras(models.Model):
    """ En cada preinscripcion el curso puede pedir datos adicionales
        particulares. Por ejemplo la lista de horarios en el que pre-inscriptio
        podría participar del curso
    """
    preinscripcion = models.ForeignKey(PreInscripcion, on_delete=models.CASCADE, related_name='extras')
    field = models.CharField(max_length=100)
    value = models.JSONField(null=True, blank=True)


class Alumno(Persona):

    matricula_id = models.CharField(max_length=100, default=generar_matricula_id)

    def __str__(self):
        return f'Alumno {self.nombres} {self.apellidos}'
