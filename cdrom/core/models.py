from django.core.exceptions import ValidationError
from django.db import models

# Códigos de paises aceptatos en el sistema
PAISES_ACEPTADOS = ['54']


class Celular(models.Model):
    """ Celulares de los usuarios """
    codigo_pais = models.CharField(max_length=5)
    codigo_area = models.CharField(max_length=10)
    numero = models.CharField(max_length=20)

    def numero_completo(self):
        """ Numero completo para mandar por plataformas de SMS """
        if self.codigo_pais == '54':
            # Argentina require un 9 antes del número
            return f"{self.codigo_pais}9{self.codigo_area}{self.numero}"
        else:
            return self.codigo_pais + self.codigo_area + self.numero

    def __str__(self):
        return f"+{self.codigo_pais} ({self.codigo_area}) {self.numero}"

    def clean_fields(self, exclude=None):
        """ Validar que el celular sea bueno para no gastar SMS en números inválidos """

        self.codigo_pais = self.codigo_pais.strip()
        self.codigo_area = self.codigo_area.strip()
        self.numero = self.numero.strip()

        if not self.codigo_pais.isdigit():
            raise ValidationError("El código de país debe contener solo números")
        if not self.codigo_area.isdigit():
            raise ValidationError("El código de área debe contener solo números")
        if not self.numero.isdigit():
            raise ValidationError("El número debe contener solo números")

        if self.codigo_pais not in PAISES_ACEPTADOS:
            raise ValidationError("El código de país no está aceptado por ahora.")

        # Argentina son siempre 10 dígitos (y el 54-9 adelanete)
        if len(self.numero_completo()) != 13:
            raise ValidationError("El número de celular no es válido")


class Persona(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    persona_id = models.CharField(max_length=120, null=True, blank=True, help_text='DNI, Cedula, RUT, etc.')
    celular_principal = models.ForeignKey(
        Celular,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='celular_principal_de'
    )
    email_principal = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
