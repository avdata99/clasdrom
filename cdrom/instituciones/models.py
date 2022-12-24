from django.db import models


class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="imgs/instituciones", null=True, blank=True)

    def __str__(self):
        return self.nombre
