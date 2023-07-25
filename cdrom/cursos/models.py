from django.db import models


class Curso(models.Model):
    institucion = models.ForeignKey("instituciones.Institucion", on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.titulo
