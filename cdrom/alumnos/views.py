from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from cursos.models import Curso
from alumnos.models import PreInscripcion, PreInscripcionExtras


@require_http_methods(["POST"])
def crear_preinscripcion(request):
    """
    Vista para crear una pre-inscripción desde el formulario de la página del curso
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)

    # Obtener datos del formulario
    nombre = data.get('fullName', '').strip()
    email = data.get('email', '').strip()
    telefono_codigo = data.get('phoneAreaCode', '').strip()
    telefono_numero = data.get('phoneNumber', '').strip()
    horarios = data.get('schedules', [])
    curso_code = data.get('courseCode')
    extra_fields = data.get('extraFields', {})

    # Validaciones básicas
    if not nombre:
        return JsonResponse({'error': 'El nombre es requerido'}, status=400)

    if not horarios:
        return JsonResponse({'error': 'Debe seleccionar al menos un horario'}, status=400)

    # Construir número de teléfono completo
    telefono_completo = ''
    if telefono_codigo and telefono_numero:
        telefono_completo = f"{telefono_codigo}-{telefono_numero}"

    # Buscar el curso
    try:
        curso = Curso.objects.get(code=curso_code)
    except Curso.DoesNotExist:
        return JsonResponse({'error': 'Curso no encontrado'}, status=404)

    try:
        # Crear la pre-inscripción
        preinscripcion = PreInscripcion.objects.create(
            curso=curso,
            nombre=nombre,
            email=email if email else None,
            telefono=telefono_completo if telefono_completo else None
        )

        # Guardar los horarios seleccionados como extras
        PreInscripcionExtras.objects.create(
            preinscripcion=preinscripcion,
            field='horarios_preferidos',
            value=horarios
        )

        # Guardar campos extra personalizados
        for field_name, field_value in extra_fields.items():
            if field_name.startswith('extra_'):
                # Remove 'extra_' prefix for storage
                clean_field_name = field_name[6:]  # Remove 'extra_' prefix
                PreInscripcionExtras.objects.create(
                    preinscripcion=preinscripcion,
                    field=clean_field_name,
                    value=field_value
                )

        # Formatear los horarios seleccionados para incluir en la respuesta
        schedule_names = {
            'wednesday_6pm': 'Miércoles 18:00 - 19:30',
            'wednesday_7_45pm': 'Miércoles 19:45 - 21:15',
            'thursday_6pm': 'Jueves 18:00 - 19:30',
            'thursday_7pm': 'Jueves 19:00 - 20:30',
            'thursday_7_45pm': 'Jueves 19:45 - 21:15',
            'friday_6pm': 'Viernes 18:00 - 19:30',
            'friday_7_45pm': 'Viernes 19:45 - 21:15',
            'saturday_9_45am': 'Sábados 09:45 - 11:15',
            'saturday_11_30am': 'Sábados 11:30 - 13:00',
            'saturday_6pm': 'Sábados 18:00 - 19:30'
        }

        horarios_nombres = [schedule_names.get(h, h) for h in horarios]

        return JsonResponse({
            'success': True,
            'codigo': preinscripcion.code,
            'nombre': preinscripcion.nombre,
            'horarios': horarios_nombres,
            'message': f'Pre-inscripción creada exitosamente. Tu código es: {preinscripcion.code}'
        })

    except Exception as e:
        return JsonResponse({'error': f'Error al crear la pre-inscripción: {str(e)}'}, status=500)
