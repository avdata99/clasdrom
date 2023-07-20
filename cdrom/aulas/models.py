from django.db import models


class Aula(models.Model):
    institucion = models.ForeignKey("instituciones.Institucion", on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    # TODO las aulas podrían tener diferentes configuraciones (con o sin mesas, etc que cambiarían su capacidad)
    capacidad_alumnos = models.IntegerField(null=True, blank=True)
    ac = models.BooleanField(default=False)
    proyector = models.BooleanField(default=False)
    pizarra = models.BooleanField(default=False)

    def primera_foto(self):
        if self.fotos.count() > 0:
            return self.fotos.first()

    def __str__(self):
        return self.nombre


class FotoAula(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="fotos")
    foto = models.ImageField(upload_to="imgs/aulas")
    orden = models.IntegerField(default=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.aula.nombre

    class Meta:
        ordering = ["orden"]
