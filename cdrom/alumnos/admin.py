from django.contrib import admin
from alumnos.models import PreInscripcion


@admin.register(PreInscripcion)
class PreInscripcionAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "telefono", "curso", "estado", "ultimo_contacto", "created")
    search_fields = ("code", "nombre", "email", "telefono", "curso__titulo")
    list_filter = ("curso", "estado", "created", "ultimo_contacto")
    readonly_fields = ("code", "created", "updated")

    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'curso', 'nombre', 'email', 'telefono')
        }),
        ('Seguimiento', {
            'fields': ('estado', 'notas_seguimiento', 'ultimo_contacto'),
            'classes': ('wide',)
        }),
        ('Fechas', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    # Acciones para cambio masivo de estado
    actions = ['marcar_como_contactado', 'marcar_como_no_responde', 'marcar_como_confirmado']

    def marcar_como_contactado(self, request, queryset):
        from django.utils import timezone
        queryset.update(estado='contactado', ultimo_contacto=timezone.now())
        self.message_user(request, f"Se marcaron {queryset.count()} pre-inscripciones como contactadas.")
    marcar_como_contactado.short_description = "Marcar como contactado"

    def marcar_como_no_responde(self, request, queryset):
        queryset.update(estado='no_responde')
        self.message_user(request, f"Se marcaron {queryset.count()} pre-inscripciones como 'no responde'.")
    marcar_como_no_responde.short_description = "Marcar como 'no responde'"

    def marcar_como_confirmado(self, request, queryset):
        from django.utils import timezone
        queryset.update(estado='confirmado', ultimo_contacto=timezone.now())
        self.message_user(request, f"Se marcaron {queryset.count()} pre-inscripciones como confirmadas.")
    marcar_como_confirmado.short_description = "Marcar como confirmado"

    def extras(self, obj):
        return ", ".join([f"{extra.field}: {extra.value}" for extra in obj.extras.all()])
    extras.short_description = "Datos adicionales"


# @admin.register(Alumno)
# class AlumnoAdmin(admin.ModelAdmin):
#     list_display = ("apellidos", "nombres", "matricula_id")
#     search_fields = ("apellidos", "nombres", "matricula_id",)
#     readonly_fields = ("matricula_id",)
