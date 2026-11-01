
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from django.contrib import messages

from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)

from django.db.models import Q
from django.db import IntegrityError
from django.db.models.deletion import (
    ProtectedError,
    RestrictedError,
)

from django.views.decorators.http import (
    require_http_methods,
    require_POST,
)

from .models import Funcionario
from .forms import FuncionarioForm


# =========================================================
# SIGED EVA 3 - GESTION DE FUNCIONARIOS
# =========================================================


# =========================================================
# LISTAR Y BUSCAR FUNCIONARIOS
# =========================================================

@login_required(login_url="login")
@permission_required(
    "funcionariosApp.view_funcionario",
    raise_exception=True
)
def inicio(request):

    busqueda = request.GET.get("q", "").strip()

    funcionarios = Funcionario.objects.select_related(
        "delegacion"
    ).all()

    # Buscar por nombre, cargo o delegacion.

    if busqueda:

        funcionarios = funcionarios.filter(
            Q(nombre__icontains=busqueda)
            | Q(cargo__icontains=busqueda)
            | Q(delegacion__nombre__icontains=busqueda)
        )

    contexto = {
        "funcionarios": funcionarios,
        "busqueda": busqueda,
    }

    return render(
        request,
        "funcionarios/inicio.html",
        contexto
    )


# =========================================================
# VER DETALLE DE FUNCIONARIO
# =========================================================

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
        "funcionario": funcionario,
    }

    return render(
        request,
        "funcionarios/detalle.html",
        contexto
    )


# =========================================================
# CREAR FUNCIONARIO
# =========================================================

@login_required(login_url="login")
@permission_required(
    "funcionariosApp.add_funcionario",
    raise_exception=True
)
@require_http_methods(["GET", "POST"])
def crear_funcionario(request):

    if request.method == "POST":

        formulario = FuncionarioForm(request.POST)

        if formulario.is_valid():

            funcionario = formulario.save()

            messages.success(
                request,
                f"El funcionario {funcionario.nombre} "
                "fue registrado correctamente."
            )

            return redirect("inicio_funcionarios")

    else:

        formulario = FuncionarioForm()

    contexto = {
        "formulario": formulario,
        "titulo": "Agregar funcionario",
        "accion": "Guardar funcionario",
    }

    return render(
        request,
        "funcionarios/formulario.html",
        contexto
    )


# =========================================================
# MODIFICAR FUNCIONARIO
# =========================================================

@login_required(login_url="login")
@permission_required(
    "funcionariosApp.change_funcionario",
    raise_exception=True
)
@require_http_methods(["GET", "POST"])
def editar_funcionario(request, id):

    funcionario = get_object_or_404(
        Funcionario,
        id=id
    )

    if request.method == "POST":

        formulario = FuncionarioForm(
            request.POST,
            instance=funcionario
        )

        if formulario.is_valid():

            funcionario = formulario.save()

            messages.success(
                request,
                f"Los datos de {funcionario.nombre} "
                "fueron actualizados correctamente."
            )

            return redirect("inicio_funcionarios")

    else:

        formulario = FuncionarioForm(
            instance=funcionario
        )

    contexto = {
        "formulario": formulario,
        "funcionario": funcionario,
        "titulo": "Modificar funcionario",
        "accion": "Guardar cambios",
    }

    return render(
        request,
        "funcionarios/formulario.html",
        contexto
    )


# =========================================================
# ELIMINAR FUNCIONARIO
# =========================================================

@login_required(login_url="login")
@permission_required(
    "funcionariosApp.delete_funcionario",
    raise_exception=True
)
@require_POST
def eliminar_funcionario(request, id):

    funcionario = get_object_or_404(
        Funcionario,
        id=id
    )

    nombre_funcionario = funcionario.nombre

    try:

        funcionario.delete()

    except (ProtectedError, RestrictedError, IntegrityError):

        messages.error(
            request,
            "No se puede eliminar este funcionario porque "
            "tiene registros relacionados que deben conservarse."
        )

    else:

        messages.success(
            request,
            f"El funcionario {nombre_funcionario} "
            "fue eliminado correctamente."
        )

    return redirect("inicio_funcionarios")
