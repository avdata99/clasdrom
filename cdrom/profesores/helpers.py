"""
Funciones adicionales del modelo
"""
from random import randint


def generar_profe_id():
    """ Generar una matrícula única de alumno"""
    from profesores.models import Profesor
    num = randint(10000, 99999)
    profe_id = f'P-{num}'
    while Profesor.objects.filter(profe_id=profe_id).count() > 0:
        num = randint(10000, 99999)
        profe_id = f'P-{num}'

    return profe_id
