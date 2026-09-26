import json

from django.conf import settings
from django.shortcuts import render


def cargar_funcionarios():

    ruta_json = settings.BASE_DIR / 'data' / 'funcionarios.json'

    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        funcionarios = json.load(archivo)

    return funcionarios


def calcular_cumplimiento(funcionario):

    meta = funcionario['meta']
    avance = funcionario['avance']

    if meta > 0:
        porcentaje = round((avance / meta) * 100)
    else:
        porcentaje = 0

    funcionario['porcentaje'] = porcentaje

    if porcentaje >= 80:
        funcionario['estado'] = 'Alto'
        funcionario['clase_estado'] = 'success'

    elif porcentaje >= 50:
        funcionario['estado'] = 'Medio'
        funcionario['clase_estado'] = 'warning'

    else:
        funcionario['estado'] = 'Bajo'
        funcionario['clase_estado'] = 'danger'

    return funcionario


def inicio(request):

    funcionarios = cargar_funcionarios()

    for funcionario in funcionarios:
        calcular_cumplimiento(funcionario)

    contexto = {
        'funcionarios': funcionarios
    }

    return render(
        request,
        'funcionarios/inicio.html',
        contexto
    )


def detalle(request, id):

    funcionarios = cargar_funcionarios()

    funcionario_encontrado = None

    for funcionario in funcionarios:

        if funcionario['id'] == id:

            funcionario_encontrado = calcular_cumplimiento(funcionario)

            break

    contexto = {
        'funcionario': funcionario_encontrado
    }

    return render(
        request,
        'funcionarios/detalle.html',
        contexto
    )