import logging
import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def send_slack_message(message):
    logger.info(f'Enviando mensaje a slack: {message}')
    message = f'*[Classdrom ENV {settings.APP_ENV}]*\n{message}'
    try:
        requests.post(settings.SLACK_WEBHOOK_URL, json={'text': message})
    except Exception as e:
        logger.error(f'Error enviando mensaje a slack: {e}')
        return False
    return True
