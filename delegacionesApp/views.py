import json

from django.conf import settings
from django.shortcuts import render


def inicio(request):

    ruta_json = settings.BASE_DIR / 'data' / 'delegaciones.json'

    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        delegaciones = json.load(archivo)

    contexto = {
        'delegaciones': delegaciones
    }

    return render(
        request,
        'delegaciones/inicio.html',
        contexto
    )


def detalle(request, nombre):

    ruta_json = settings.BASE_DIR / 'data' / 'delegaciones.json'

    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        delegaciones = json.load(archivo)

    delegacion_encontrada = None

    for delegacion in delegaciones:

        if delegacion['nombre'].lower() == nombre.lower():
            delegacion_encontrada = delegacion
            break

    contexto = {
        'delegacion': delegacion_encontrada
    }

    return render(
        request,
        'delegaciones/detalle.html',
        contexto
    )