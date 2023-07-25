from django.db import models
from profesores.helpers import generar_profe_id
from core.models import Persona


class Profesor(Persona):

    profe_id = models.CharField(max_length=100, default=generar_profe_id)

    def __str__(self):
        return f'Profe {self.nombres} {self.apellidos}'
