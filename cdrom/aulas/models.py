from django.db import models


class Aula(models.Model):
    institucion = models.ForeignKey("instituciones.Institucion", on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    capacidad_alumnos = models.IntegerField(default=0)

    def primera_foto(self):
        if self.fotos.count() > 0:
            return self.fotos.first()

    def __str__(self):
        return self.nombre


class FotoAula(models.Model):
    """ Fotos en cada formato """
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="fotos")
    foto = models.ImageField(upload_to="imgs/aulas")
    orden = models.IntegerField(default=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Foto {self.aula.nombre} {self.orden}'

    class Meta:
        ordering = ["orden"]


class CaracteristicaAula(models.Model):
    """ Fotos en cada formato """
    nombre = models.CharField(max_length=100, help_text="Por ejemplo AC, Proyector, Pizarra, etc.")


class CaracteristicaEnAula(models.Model):
    """ Fotos en cada formato """
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="caracteristicas")
    caracteristica = models.ForeignKey(CaracteristicaAula, related_name='en_aulas')
    descripcion = models.TextField(null=True, blank=True)
    disponible = models.BooleanField(default=True, help_text='Está disponible?')
    se_debe_pedir = models.BooleanField(default=False, help_text='No es una caracteristica fija y se debe pedir?')
    orden = models.IntegerField(default=100)

    class Meta:
        # no definir dos veces la misma caracteristica en la misma aula
        unique_together = ('aula', 'caracteristica')
        ordering = ["orden"]
