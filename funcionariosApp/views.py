from django.shortcuts import render, get_object_or_404
from .models import Funcionario


def inicio(request):
    # Obtener funcionarios desde MySQL mediante Django ORM
    funcionarios = Funcionario.objects.select_related('delegacion').all()

    return render(
        request,
        'funcionarios/inicio.html',
        {
            'funcionarios': funcionarios
        }
    )


def detalle(request, id):
    # Obtener un funcionario específico desde MySQL
    funcionario = get_object_or_404(
        Funcionario.objects.select_related('delegacion'),
        id=id
    )

    return render(
        request,
        'funcionarios/detalle.html',
        {
            'funcionario': funcionario
        }
    )