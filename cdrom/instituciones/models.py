from django.contrib.sites.models import Site
from django.db import models


class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="imgs/instituciones", null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre


class FotoInstitucion(models.Model):
    """ Fotos en cada formato """
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name="fotos")
    foto = models.ImageField(upload_to="imgs/instituciones")
    orden = models.IntegerField(default=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Foto {self.institucion.nombre} {self.orden}'

    class Meta:
        ordering = ["orden"]
