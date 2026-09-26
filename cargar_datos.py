import os
import json
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from delegacionesApp.models import Delegacion
from funcionariosApp.models import Funcionario


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def cargar_delegaciones():
    ruta = os.path.join(BASE_DIR, 'data', 'delegaciones.json')

    with open(ruta, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    for item in datos:
        delegacion, creada = Delegacion.objects.update_or_create(
            nombre=item['nombre'],
            defaults={
                'sector': item['sector'],
                'descripcion': item['descripcion'],
            }
        )

        if creada:
            print(f"Delegación creada: {delegacion.nombre}")
        else:
            print(f"Delegación actualizada: {delegacion.nombre}")


def cargar_funcionarios():
    ruta = os.path.join(BASE_DIR, 'data', 'funcionarios.json')

    with open(ruta, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    for item in datos:
        try:
            delegacion = Delegacion.objects.get(
                nombre=item['delegacion']
            )

            funcionario, creado = Funcionario.objects.update_or_create(
                nombre=item['nombre'],
                defaults={
                    'cargo': item['cargo'],
                    'delegacion': delegacion,
                    'meta': item['meta'],
                    'avance': item['avance'],
                }
            )

            if creado:
                print(f"Funcionario creado: {funcionario.nombre}")
            else:
                print(f"Funcionario actualizado: {funcionario.nombre}")

        except Delegacion.DoesNotExist:
            print(
                f"ERROR: No existe la delegación "
                f"{item['delegacion']} para {item['nombre']}"
            )


if __name__ == '__main__':
    print("=== INICIANDO MIGRACIÓN JSON → MYSQL ===")

    cargar_delegaciones()
    cargar_funcionarios()

    print()
    print("=== MIGRACIÓN FINALIZADA ===")
    print(f"Delegaciones en BD: {Delegacion.objects.count()}")
    print(f"Funcionarios en BD: {Funcionario.objects.count()}")