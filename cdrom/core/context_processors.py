from django.conf import settings
# from django.urls import reverse
# from core.context_menues import global_menu_context


def app_base_context(request):
    """ Contexto para todos los templates con datos de esta aplicacion """
    # Build WhatsApp URL
    country = settings.APP_WHATSAPP_COUNTRY_CODE
    zone = settings.APP_WHATSAPP_ZONE_CODE
    number = settings.APP_WHATSAPP_NUMBER

    # Arg numbers requires a "9" at the beginning
    if country == "54" and zone.startswith("9") is False:
        zone = "9" + zone
    whatsapp_number = f"+{country}{zone}{number}"
    whatsapp_message = "Hola ..."
    whatsapp_url = f"https://wa.me/{country}{zone}{number}?text={whatsapp_message}"

    instagram_name = settings.APP_INSTAGRAM
    instagram_url = f"https://instagram.com/{instagram_name}"
    youtube_channel = settings.APP_YOUTUBE_CHANNEL
    youtube_url = f"https://youtube.com/{youtube_channel}"

    email = settings.APP_EMAIL

    return {
        'app_version': settings.APP_VERSION,
        'site_brand': settings.APP_LABEL,
        'site_email': settings.APP_EMAIL,
        'site_url': settings.APP_URL,
        'whatsapp_number': whatsapp_number,
        'whatsapp_url': whatsapp_url,
        'instagram_name': instagram_name,
        'instagram_url': instagram_url,
        'youtube_channel': youtube_channel,
        'youtube_url': youtube_url,
        'email': email,
        # Menues del header
        # 'menues': global_menu_context(),
        }
