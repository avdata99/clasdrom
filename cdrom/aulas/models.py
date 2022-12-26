from django.db import models


class Aula(models.Model):
    institucion = models.ForeignKey("instituciones.Institucion", on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    # TODO las aulas podrían tener diferentes configuraciones (con o sin mesas, etc que cambiarían su capacidad)
    capacidad_alumnos = models.IntegerField(null=True, blank=True)
    ac = models.BooleanField(default=False)
    proyector = models.BooleanField(default=False)
    pizarra = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
