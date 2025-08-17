from django.contrib import admin
from alumnos.models import PreInscripcion


@admin.register(PreInscripcion)
class PreInscripcionAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "email", "telefono", "curso", "created", "extras")
    search_fields = ("code", "nombre", "email", "telefono", "curso__nombre")
    list_filter = ("curso", )
    readonly_fields = ("code", )

    def extras(self, obj):
        return ", ".join([f"{extra.field}: {extra.value}" for extra in obj.extras.all()])
    extras.short_description = "Datos adicionales"


# @admin.register(Alumno)
# class AlumnoAdmin(admin.ModelAdmin):
#     list_display = ("apellidos", "nombres", "matricula_id")
#     search_fields = ("apellidos", "nombres", "matricula_id",)
#     readonly_fields = ("matricula_id",)
