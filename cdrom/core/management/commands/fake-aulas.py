import random
from django.core.management.base import BaseCommand
from aulas.models import Aula, CaracteristicaAula, CaracteristicaEnAula


class Command(BaseCommand):
    help = 'Inventar aulas y sus características para la base de datos'

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=50, help="How many aulas?")

    def _fake_aula(self):
        letters = 'aaaabcdeeeeefimmmmmnoprstu '
        name_length = random.randint(5, 10)
        name = ''.join(random.choice(letters) for _ in range(name_length))
        descripcion = "Descripción de " + name

        aula = Aula.objects.create(
            nombre=name,
            descripcion=descripcion,
            capacidad_alumnos=random.randint(10, 50),
        )
        return aula

    # def _agregar_fotos(self, aula):
    #     for i in range(random.randint(1, 3)):
    #         foto = FotoAula.objects.create(
    #             aula=aula,
    #             foto=f"imgs/aulas/aula_{aula.id}_foto{i}.jpg",
    #             orden=i,
    #             descripcion=f"Descripción de la foto {i}",
    #         )

    def _crear_caracteristicas(self):
        nombres_caracteristicas = ["AC", "Proyector", "Pizarra", "Sillas ergonómicas", "Ventanas grandes"]
        for nombre in nombres_caracteristicas:
            CaracteristicaAula.objects.get_or_create(nombre=nombre)

    def _agregar_caracteristicas(self, aula):
        caracteristicas = CaracteristicaAula.objects.all()
        for caracteristica in caracteristicas:
            CaracteristicaEnAula.objects.create(
                aula=aula,
                caracteristica=caracteristica,
                descripcion=f"Descripción de la característica {caracteristica.nombre}",
                disponible=random.choice([True, False]),
                se_debe_pedir=random.choice([True, False]),
                orden=random.randint(1, 100),
            )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Agregando aulas y características ficticias'))
        self._crear_caracteristicas()

        for _ in range(options['total']):
            aula = self._fake_aula()
            self._agregar_fotos(aula)
            self._agregar_caracteristicas(aula)

            self.stdout.write(self.style.SUCCESS(f' - Aula {aula.nombre} creada'))

        self.stdout.write(self.style.SUCCESS('Terminado'))
