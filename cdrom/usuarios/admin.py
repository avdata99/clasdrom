from django.contrib import admin
from usuarios.models import ClasdromUsuario, ClasdromUserAction


@admin.register(ClasdromUsuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'celular', 'created_at')
    list_per_page = 10
    search_fields = ('user__email', 'user__username')


@admin.register(ClasdromUserAction)
class ClassDromUserActionAdmin(admin.ModelAdmin):
    list_display = (
        'clasdrom_user', 'action', 'generic_text1',
        'generic_text2', 'generic_number1', 'generic_number2',
        'created_at', 'ip', 'user_agent',
    )
    list_filter = ('action', 'clasdrom_user')
    list_per_page = 10
