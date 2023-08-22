from django.contrib.auth.models import User
from django.db import models
from usuarios.enums import UserAction


class ClasdromUsuario(models.Model):
    """ Usuarios internos, para colocar las propiedades personalizadas de los usuarios del sistema """
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='clasdrom_user')
    # TODO posiblemente necesitemos celulares extras para los usuarios
    celular = models.ForeignKey("core.Celular", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Si viene de login con otro prtoveedor
    provider = models.CharField(max_length=20, null=True, blank=True)
    provider_id = models.CharField(max_length=255, null=True, blank=True)
    provider_picture_url = models.URLField(null=True, blank=True)
    provider_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class ClasdromUserAction(models.Model):
    """ Acciones que realiza un usuario en la aplicación. """
    clasdrom_user = models.ForeignKey(ClasdromUsuario, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=2, choices=UserAction.choices)
    # Cada accion puede tener un par de textos/numeros genericos con diferente funcionalidad en cada accion
    generic_text1 = models.CharField(max_length=255, null=True, blank=True)
    generic_text2 = models.CharField(max_length=255, null=True, blank=True)
    generic_number1 = models.IntegerField(null=True, blank=True)
    generic_number2 = models.IntegerField(null=True, blank=True)
    # Datos extras de la accion
    data = models.JSONField(null=True, blank=True)
    # Si corresponde, datos del request
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.clasdrom_user} - {self.action}'

    @classmethod
    def log_action(cls, request, action, **kwargs):
        """ Registrar una accion de un usuario (de Django) definido"""

        # En la signal de logged in, el request no tiene user
        # pero si tengo un parámetroi aparte llamado user
        # Opcionalmente usamos este via los KWARGS genericos que tenemos aca
        if not hasattr(request, 'user'):
            user = kwargs.get('user')
        else:
            user = request.user

        # verificar que el usuario tenga un clasdrom_user
        if not hasattr(user, 'clasdrom_user'):
            # crear el classdrom  user
            ClasdromUsuario.objects.create(user=user)

        # crear la accion
        sua = cls.objects.create(
            clasdrom_user=user.clasdrom_user,
            action=action,
        )
        if kwargs.get('generic_text1'):
            sua.generic_text1 = kwargs['generic_text1']
        if kwargs.get('generic_text2'):
            sua.generic_text2 = kwargs['generic_text2']
        if kwargs.get('generic_number1'):
            sua.generic_number1 = kwargs['generic_number1']
        if kwargs.get('generic_number2'):
            sua.generic_number2 = kwargs['generic_number2']
        if kwargs.get('data'):
            sua.data = kwargs['data']

        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            ip = user_ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        sua.ip = ip
        sua.user_agent = request.META.get('HTTP_USER_AGENT', 'NO-UA')
        sua.save()
