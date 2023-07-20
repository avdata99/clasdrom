from django.core.management.base import BaseCommand

from aulas.helpers import init_caracteristicas


class Command(BaseCommand):
    help = 'Inicializar los datos del sistema'

    def add_arguments(self, parser):
        parser.add_argument("--clean-all", help="Limpiar todo antes de cargar datos", action='store_true')

    def handle(self, *args, **options):  # noqa C901
        self.stdout.write(self.style.SUCCESS('Inicializando datos del sistema'))
        clean_all = options.get('clean_all')
        # TODO, hacer el clean all
        if clean_all:
            raise NotImplementedError()

        # Ejecutar todas las funciones de inicializacion
        init_caracteristicas()

        self.stdout.write(self.style.SUCCESS('Inicialición terminada'))
