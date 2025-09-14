"""
Funciones adicionales del modelo
"""
from random import randint


def generar_pre_inscripcion_id(curso, start=23):
    """ Generar un codigo unico a un pre-inscripto basado en el código
        del curso mas una autonumeracion que comienza en <start>
    """
    from alumnos.models import PreInscripcion
    fill_length = 3
    # ensure 3 digits
    num = str(start).zfill(fill_length)
    base = start
    pre_inscripcion_id = f'{curso.code}-{num}'
    while PreInscripcion.objects.filter(code=pre_inscripcion_id).count() > 0:
        base += 1
        # if num >= 1000, then use 4 digits
        if base >= (10 ** fill_length) - 1:
            fill_length += 1
        num = str(base).zfill(fill_length)
        pre_inscripcion_id = f'{curso.code}-{num}'

    return pre_inscripcion_id


def generar_matricula_id():
    """ Generar una matrícula única de alumno"""
    from alumnos.models import Alumno
    num = randint(10000, 99999)
    matricula_id = f'A-{num}'
    while Alumno.objects.filter(matricula_id=matricula_id).count() > 0:
        num = randint(10000, 99999)
        matricula_id = f'A-{num}'

    return matricula_id
