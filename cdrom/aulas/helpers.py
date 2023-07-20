"""
Funciones adicionales del modelo
"""
import logging
from aulas.models import CaracteristicaAula


logger = logging.getLogger(__name__)


def init_caracteristicas():
    """ Inicializar las características basicas del sistema """

    logger.info('Inicializando caracteristica del sistema')

    caracteristicas = [
        'Aire acondicionado Frio',
        'Aire acondicionado Calor',
        'Proyector',
        'Pizarra',
    ]

    for carac in caracteristicas:
        _, created = CaracteristicaAula.objects.get_or_create(
            nombre=carac,
        )
        logger.info(f'Inicializando caracteristica {carac} (creado={created})')
