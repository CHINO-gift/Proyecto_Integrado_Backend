
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (
    login_required,
    permission_required
)

from .models import Funcionario


# ==========================================
# EVA 3 - MODULO DE FUNCIONARIOS
# ==========================================


# ==========================================
# LISTADO DE FUNCIONARIOS
# ==========================================

@login_required(login_url="login")
@permission_required(
    "funcionariosApp.view_funcionario",
    raise_exception=True
)
def inicio(request):

    funcionarios = Funcionario.objects.select_related(
        "delegacion"
    ).all()

    contexto = {
        "funcionarios": funcionarios
    }

    return render(
        request,
        "funcionarios/inicio.html",
        contexto
    )


# ==========================================
# DETALLE DE FUNCIONARIO
# ==========================================

@login_required(login_url="login")
@permission_required(
    "funcionariosApp.view_funcionario",
    raise_exception=True
)
def detalle(request, id):

    funcionario = get_object_or_404(
        Funcionario.objects.select_related(
            "delegacion"
        ),
        id=id
    )

    contexto = {
        "funcionario": funcionario
    }

    return render(
        request,
        "funcionarios/detalle.html",
        contexto
    )
