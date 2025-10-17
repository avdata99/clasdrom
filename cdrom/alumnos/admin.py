from django.contrib import admin
from alumnos.models import PreInscripcion, PreInscripcionExtras
import csv
from django.http import HttpResponse


@admin.register(PreInscripcion)
class PreInscripcionAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "telefono", "curso", "estado", "notas_seguimiento", "extras")
    search_fields = ("code", "nombre", "email", "telefono", "curso__titulo")
    list_filter = ("curso", "estado", "created", "ultimo_contacto")
    readonly_fields = ("code", "created", "updated")
    ordering = ['-created']

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
    actions = ['marcar_como_contactado', 'marcar_como_no_responde', 'marcar_como_confirmado', 'export_to_csv']

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

    def changelist_view(self, request, extra_context=None):
        """Add horarios_preferidos statistics to the changelist view"""
        extra_context = extra_context or {}

        # Get pre-inscriptions grouped by curso
        curso_stats = []
        cursos = self.model.objects.values_list('curso', flat=True).distinct()

        for curso_id in cursos:
            if curso_id is None:
                continue

            curso = self.model.objects.filter(curso_id=curso_id).first().curso

            # Get pre-inscriptions for this curso that have horarios_preferidos
            curso_preinscripciones = self.model.objects.filter(
                curso_id=curso_id,
                extras__field='horarios_preferidos'
            ).select_related('curso').prefetch_related('extras')

            if not curso_preinscripciones.exists():
                continue

            # Get all unique horarios_preferidos values
            horarios_extras = PreInscripcionExtras.objects.filter(
                field='horarios_preferidos',
                preinscripcion__curso_id=curso_id,
            )
            # horarios_preferidos is a list, detect all values with no duplicates and sort them
            values = set()
            for horario in horarios_extras:
                for value in horario.value if isinstance(horario.value, list) else [horario.value]:
                    values.add(value)
            horarios_values = sorted(values)

            # Build table data
            table_data = []
            horarios_totals = {horario: 0 for horario in horarios_values}

            for preinscripcion in curso_preinscripciones:
                row = {'nombre': preinscripcion.nombre}

                # Fill in the horarios for this pre-inscription
                pi_hor = preinscripcion.extras.filter(field='horarios_preferidos').first()
                if pi_hor:
                    for value in pi_hor.value:
                        row[value] = 'X'
                        horarios_totals[value] += 1

                table_data.append(row)

            curso_stats.append({
                'curso': curso,
                'table_data': table_data,
                'horarios': horarios_values,
                'totals': horarios_totals,
                'total_count': len(table_data)
            })

        extra_context.update({
            'curso_horarios_stats': curso_stats,
        })

        return super().changelist_view(request, extra_context)

    def export_to_csv(self, request, queryset):
        """Export selected pre-inscripciones to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="preinscripciones.csv"'

        writer = csv.writer(response)
        # Write header
        writer.writerow([
            'Código', 'Nombre', 'Email', 'Teléfono', 'Curso',
            'Estado', 'Notas de Seguimiento', 'Último Contacto',
            'Fecha Creación', 'Datos Adicionales'
        ])

        # Write data rows
        for obj in queryset.select_related('curso').prefetch_related('extras'):
            extras_str = "; ".join([f"{extra.field}: {extra.value}" for extra in obj.extras.all()])
            writer.writerow([
                obj.code,
                obj.nombre,
                obj.email,
                obj.telefono,
                obj.curso.titulo if obj.curso else '',
                obj.get_estado_display() if hasattr(obj, 'get_estado_display') else obj.estado,
                obj.notas_seguimiento or '',
                obj.ultimo_contacto.strftime('%Y-%m-%d %H:%M') if obj.ultimo_contacto else '',
                obj.created.strftime('%Y-%m-%d %H:%M') if obj.created else '',
                extras_str
            ])

        return response

    export_to_csv.short_description = "Exportar a CSV"


@admin.register(PreInscripcionExtras)
class PreInscripcionExtrasAdmin(admin.ModelAdmin):
    list_display = ("preinscripcion", "field", "value")
    search_fields = ("preinscripcion__nombre", "field", "value")
    list_filter = ("field",)
    ordering = ['-preinscripcion__created']


# @admin.register(Alumno)
# class AlumnoAdmin(admin.ModelAdmin):
#     list_display = ("apellidos", "nombres", "matricula_id")
#     search_fields = ("apellidos", "nombres", "matricula_id",)
#     readonly_fields = ("matricula_id",)
