from django.db import models
from alumnos.helpers import generar_matricula_id, generar_pre_inscripcion_id
from core.models import Persona
from cursos.models import Curso


class PreInscripcion(models.Model):
    """ Primera instancia generica donde tomamos datos sin mucha validacion
        Esto es para el formulario de pre-inscripcion y va a requerir trabajo
        para procesarlo, conversar con un interesado y convencerlo de que se inscriba.
    """

    # Estados del lead/pre-inscripto
    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo - Sin contactar'),
        ('contactado', 'Contactado'),
        ('interesado', 'Interesado - Respondió positivamente'),
        ('dudoso', 'Dudoso - Necesita más información'),
        ('confirmado', 'Confirmado - Listo para inscribirse'),
        ('inscripto', 'Inscripto - Ya es alumno'),
        ('no_interesado', 'No interesado'),
        ('no_responde', 'No responde'),
    ]

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    # Le vamos a dar un codigo único a cada preinscripto
    code = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    # Estado del seguimiento
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='nuevo',
        help_text="Estado actual del seguimiento del lead"
    )

    # Notas para el seguimiento
    notas_seguimiento = models.TextField(
        null=True,
        blank=True,
        help_text="Notas sobre las conversaciones y seguimiento del lead"
    )

    # Fecha del último contacto
    ultimo_contacto = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha y hora del último contacto con el lead"
    )

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
