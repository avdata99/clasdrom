from django.db import models
from alumnos.helpers import generar_matricula_id
from core.models import Persona


class Alumno(Persona):

    matricula_id = models.CharField(max_length=100, default=generar_matricula_id)

    def __str__(self):
        return f'Alumno {self.nombres} {self.apellidos}'
