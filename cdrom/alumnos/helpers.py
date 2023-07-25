"""
Funciones adicionales del modelo
"""
from random import randint


def generar_matricula_id():
    """ Generar una matrícula única de alumno"""
    from alumnos.models import Alumno
    num = randint(10000, 99999)
    matricula_id = f'A-{num}'
    while Alumno.objects.filter(matricula_id=matricula_id).count() > 0:
        num = randint(10000, 99999)
        matricula_id = f'A-{num}'

    return matricula_id
