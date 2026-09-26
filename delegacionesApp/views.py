from django.shortcuts import render, get_object_or_404
from .models import Delegacion


def inicio(request):
    # Obtener todas las delegaciones desde MySQL mediante Django ORM
    delegaciones = Delegacion.objects.all()

    return render(
        request,
        'delegaciones/inicio.html',
        {
            'delegaciones': delegaciones
        }
    )


def detalle(request, id):
    # Obtener una delegación específica desde MySQL
    delegacion = get_object_or_404(Delegacion, id=id)

    return render(
        request,
        'delegaciones/detalle.html',
        {
            'delegacion': delegacion
        }
    )