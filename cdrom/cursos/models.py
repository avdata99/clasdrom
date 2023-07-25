from django.db import models


class Curso(models.Model):
    institucion = models.ForeignKey("instituciones.Institucion", on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    # TODO las aulas podrían tener diferentes configuraciones (con o sin mesas, etc que cambiarían su capacidad)
    capacidad_alumnos = models.IntegerField(null=True, blank=True)
    objetivo_general = models.TextField(null=True, blank=True)
    objetivos_especificos = models.TextField(null=True, blank=True)
    temario = models.TextField(null=True, blank=True)
    destinatarios = models.TextField(null=True, blank=True)
    requisitos = models.TextField(null=True, blank=True)
    equipo_docente = models.TextField(null=True, blank=True)
    bibliografia = models.TextField(null=True, blank=True)
    certificacion = models.TextField(null=True, blank=True)
    metodologia = models.TextField(null=True, blank=True)
    evalucacion = models.TextField(null=True, blank=True)

    def primera_foto(self):
        if self.fotos.count() > 0:
            return self.fotos.first()

    def __str__(self):
        return self.nombre


class FotoCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="fotos")
    foto = models.ImageField(upload_to="imgs/cursos")
    orden = models.IntegerField(default=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.aula.nombre

    class Meta:
        ordering = ["orden"]
