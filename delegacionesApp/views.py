
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (
    login_required,
    permission_required
)

from .models import Delegacion


# ==========================================
# EVA 3 - MODULO DE DELEGACIONES
# ==========================================


# ==========================================
# LISTADO DE DELEGACIONES
# ==========================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.view_delegacion",
    raise_exception=True
)
def inicio(request):

    # Obtener todas las delegaciones
    # utilizando Django ORM.

    delegaciones = Delegacion.objects.all()

    contexto = {
        "delegaciones": delegaciones
    }

    return render(
        request,
        "delegaciones/inicio.html",
        contexto
    )


# ==========================================
# DETALLE DE DELEGACION
# ==========================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.view_delegacion",
    raise_exception=True
)
def detalle(request, nombre):

    # Buscar la delegacion por su nombre.

    delegacion = get_object_or_404(
        Delegacion,
        nombre=nombre
    )

    contexto = {
        "delegacion": delegacion
    }

    return render(
        request,
        "delegaciones/detalle.html",
        contexto
    )
