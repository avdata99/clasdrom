import logging
from hashlib import md5
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
from core.notifications.notify import send_slack_message
from usuarios.models import ClasdromUsuario


logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@csrf_exempt
def google_login_callback(request):
    """ Callback de Google Login.
        Process data from Google and get the user token
        This is a POST call with this payload
        credential: XXXX
        g_csrf_token: ABC
        Also, Cookie: csrftoken=YYY; G_ENABLED_IDPS=google; g_state={"i_l":0}; g_csrf_token=ABC
    """

    # Verify cookie
    csrf_token_cookie = request.COOKIES.get('g_csrf_token')
    if not csrf_token_cookie:
        return HttpResponseBadRequest('No CSRF token in Cookie.')
    csrf_token_body = request.POST.get('g_csrf_token')
    if not csrf_token_body:
        return HttpResponseBadRequest('No CSRF token in post body.')
    if csrf_token_cookie != csrf_token_body:
        return HttpResponseBadRequest('Failed to verify double submit cookie.')

    google_request = g_requests.Request()
    creds = request.POST['credential']
    try:
        # Verify the token / credential
        idinfo = id_token.verify_oauth2_token(creds, google_request, settings.GOOGLE_CLIENT_ID)

        if idinfo['aud'] != settings.GOOGLE_CLIENT_ID:
            logger.error(f"idinfo['aud'] != settings.GOOGLE_CLIENT_ID :: {idinfo['aud']} != {settings.GOOGLE_CLIENT_ID}")

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        """
        {
            'iss': 'https://accounts.google.com',
            'nbf': 16829XXX,
            'aud': '926205898372-3qk962hjq12f8jp8n1jg1s5o0vo14jjr.apps.googleusercontent.com',
            'sub': '10221742XXXX',
            'email': 'algo@gmail.com',
            'email_verified': True,
            'azp': '926205898372-3qk962hjq12f8jp8n1jg1s5o0vo14jjr.apps.googleusercontent.com',
            'name': 'Cluster INC',
            'picture': 'https://lh3.googleusercontent.com/a/xxxx',
            'given_name': 'Cluster',
            'family_name': 'INC',
            'iat': 16829XXX,
            'exp': 16829XXXX,
            'jti': '6789c2d8XXXX'
        }
        """
        userid = idinfo['sub']
        logger.info(f'Google login callback user id: {userid} :: {idinfo}')
    except ValueError:
        # Invalid token
        logger.error(f'Invalid token "{csrf_token_cookie}" "{csrf_token_body}"')
        return HttpResponseBadRequest('Invalid token')

    provider = 'GOOGLE'
    provider_id = idinfo.pop('sub')
    provider_picture_url = idinfo.pop('picture', None)
    email = idinfo.pop('email')
    first_name = idinfo.pop('given_name', None)
    last_name = idinfo.pop('family_name', None)

    # ver si el usuario ya existe
    clasdrom_user = ClasdromUsuario.objects.filter(
        provider=provider,
        provider_id=provider_id
    ).first()
    # Si no existe, crear un nuevo usuario
    if clasdrom_user is None:
        send_slack_message(f'Nuevo usuario de Google regisytrado en el sitio: {first_name} {last_name} :: {email}')
        internal_name = f'google_{userid}'
        user = User(
            username=internal_name,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=md5(internal_name.encode('utf-8')).hexdigest()
        )
        # Ya hay una señal (signal) que creara el user.
        # Necesitamos darle los datos de google
        user._provider = 'GOOGLE'
        user._provider_id = userid
        user._provider_picture_url = provider_picture_url
        user._provider_data = idinfo
        user.save()
    else:
        logger.info(f'Google login callback user already exists: {clasdrom_user}')
        user = clasdrom_user.user

    # Loguear de prepo al usuario
    login(request, user)

    return redirect('base')
