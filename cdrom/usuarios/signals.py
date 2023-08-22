import logging
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from usuarios.models import ClasdromUsuario
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from usuarios.models import ClasdromUserAction
from usuarios.enums import UserAction


logger = logging.getLogger(__name__)


def create_profile(sender, instance, created, **kwargs):
    if created:
        # Algunos usuarios vienen de proveedores externos, en esos casos
        # tomar estos datos
        provider = instance._provider if hasattr(instance, '_provider') else None
        provider_id = instance._provider_id if hasattr(instance, '_provider_id') else None
        provider_picture_url = instance._provider_picture_url if hasattr(instance, '_provider_picture_url') else None
        provider_data = instance._provider_data if hasattr(instance, '_provider_data') else None
        ClasdromUsuario.objects.create(
            user=instance,
            provider=provider,
            provider_id=provider_id,
            provider_picture_url=provider_picture_url,
            provider_data=provider_data
        )
        logger.info(f'ClasdromUsuario was created successfully: {instance.email}')


post_save.connect(create_profile, sender=User)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ClasdromUserAction.log_action(request, action=UserAction.LOGIN, user=user)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ClasdromUserAction.log_action(request, action=UserAction.LOGOUT, user=user)
