
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Delegacion


# ==========================================
# EVA 3 - MÓDULO DE DELEGACIONES
# ==========================================


# ==========================================
# LISTADO DE DELEGACIONES
# ==========================================

@login_required(login_url='login')
def inicio(request):

    # Obtener todas las delegaciones
    # utilizando Django ORM

    delegaciones = Delegacion.objects.all()

    contexto = {
        'delegaciones': delegaciones
    }

    return render(
        request,
        'delegaciones/inicio.html',
        contexto
    )


# ==========================================
# DETALLE DE DELEGACIÓN
# ==========================================

@login_required(login_url='login')
def detalle(request, nombre):

    # Obtener una delegación por su nombre

    delegacion = get_object_or_404(
        Delegacion,
        nombre=nombre
    )

    contexto = {
        'delegacion': delegacion
    }

    return render(
        request,
        'delegaciones/detalle.html',
        contexto
    )
