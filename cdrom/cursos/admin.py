from django.contrib import admin
from cursos.models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("code", "titulo", "descripcion")
    search_fields = ("titulo", "descripcion")
