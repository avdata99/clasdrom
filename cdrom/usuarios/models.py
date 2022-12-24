from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    """ Usuarios internos, para colocar las propiedades personalizadas de los usuarios del sistema """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO posiblemente necesitemos celulares extras para los usuarios
    celular = models.ForeignKey("core.Celular", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
