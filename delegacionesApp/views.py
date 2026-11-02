
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)

from django.contrib import messages

from django.core.exceptions import PermissionDenied

from django.db import transaction
from django.db.models import Q

from django.db.models.deletion import (
    ProtectedError,
    RestrictedError,
)

from django.views.decorators.http import (
    require_http_methods,
    require_POST,
)

from .models import Delegacion
from .forms import DelegacionForm
from .forms_operacion import FuncionarioInicialForm


# =========================================================
# SIGED EVA 3 - MODULO DE DELEGACIONES
# =========================================================


# =========================================================
# LISTAR Y BUSCAR DELEGACIONES
# Permiso: consultar delegaciones
# =========================================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.view_delegacion",
    raise_exception=True
)
def inicio(request):

    delegaciones = Delegacion.objects.all()

    busqueda = request.GET.get("q", "").strip()

    if busqueda:
        delegaciones = delegaciones.filter(
            Q(nombre__icontains=busqueda)
            | Q(sector__icontains=busqueda)
        )

    contexto = {
        "delegaciones": delegaciones,
        "busqueda": busqueda,
    }

    return render(
        request,
        "delegaciones/inicio.html",
        contexto
    )


# =========================================================
# DETALLE DE DELEGACION
# Permiso: consultar delegaciones
# =========================================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.view_delegacion",
    raise_exception=True
)
def detalle(request, nombre):

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


# =========================================================
# CREAR DELEGACION
# Permiso: agregar delegaciones
#
# EVA 3:
# Permite agregar opcionalmente un funcionario inicial.
#
# Si se registra un funcionario, ambas entidades
# se guardan mediante una transaccion atomica.
# =========================================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.add_delegacion",
    raise_exception=True
)
@require_http_methods(["GET", "POST"])
def crear_delegacion(request):

    # Verificar si el usuario puede crear funcionarios.
    puede_agregar_funcionario = request.user.has_perm(
        "funcionariosApp.add_funcionario"
    )

    # La casilla se enviara desde el formulario HTML.
    incluir_funcionario = (
        request.method == "POST"
        and request.POST.get("incluir_funcionario") == "on"
    )

    # Si se solicita crear un funcionario, el usuario
    # debe tener permisos de creacion sobre esa entidad.
    if incluir_funcionario and not puede_agregar_funcionario:
        raise PermissionDenied(
            "No tienes permisos para registrar funcionarios."
        )

    if request.method == "POST":

        # Formulario original de delegaciones.
        formulario = DelegacionForm(
            request.POST
        )

        # Formulario adicional de funcionario.
        # Solo se valida cuando se marca la casilla.
        formulario_funcionario = FuncionarioInicialForm(
            request.POST if incluir_funcionario else None,
            prefix="funcionario"
        )

        # Validamos los formularios antes de guardar.
        delegacion_valida = formulario.is_valid()

        funcionario_valido = True

        if incluir_funcionario:
            funcionario_valido = (
                formulario_funcionario.is_valid()
            )

        if delegacion_valida and funcionario_valido:

            if incluir_funcionario:

                # =========================================
                # EVA 3 - TRANSACCION ENTRE DOS ENTIDADES
                # =========================================

                with transaction.atomic():

                    # 1. Registrar la delegacion.
                    delegacion = formulario.save()

                    # 2. Preparar funcionario inicial.
                    funcionario = (
                        formulario_funcionario.save(
                            commit=False
                        )
                    )

                    # 3. Relacionar funcionario y delegacion.
                    funcionario.delegacion = delegacion

                    # 4. Registrar funcionario.
                    funcionario.save()

                messages.success(
                    request,
                    (
                        f"La delegación '{delegacion.nombre}' "
                        f"y el funcionario '{funcionario.nombre}' "
                        "fueron registrados correctamente."
                    )
                )

            else:

                # =========================================
                # REGISTRO NORMAL DE DELEGACION
                # =========================================

                delegacion = formulario.save()

                messages.success(
                    request,
                    f"La delegación '{delegacion.nombre}' "
                    "fue registrada correctamente."
                )

            return redirect(
                "inicio_delegaciones"
            )

    else:

        formulario = DelegacionForm()

        formulario_funcionario = FuncionarioInicialForm(
            prefix="funcionario"
        )

    contexto = {
        "formulario": formulario,
        "formulario_funcionario": formulario_funcionario,
        "titulo": "Agregar delegación",
        "accion": "Agregar",
        "es_creacion": True,
        "incluir_funcionario": incluir_funcionario,
        "puede_agregar_funcionario": puede_agregar_funcionario,
    }

    return render(
        request,
        "delegaciones/formulario.html",
        contexto
    )


# =========================================================
# MODIFICAR DELEGACION
# Permiso: modificar delegaciones
# =========================================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.change_delegacion",
    raise_exception=True
)
@require_http_methods(["GET", "POST"])
def editar_delegacion(request, pk):

    delegacion = get_object_or_404(
        Delegacion,
        pk=pk
    )

    if request.method == "POST":

        formulario = DelegacionForm(
            request.POST,
            instance=delegacion
        )

        if formulario.is_valid():

            delegacion = formulario.save()

            messages.success(
                request,
                f"La delegación '{delegacion.nombre}' "
                "fue modificada correctamente."
            )

            return redirect(
                "inicio_delegaciones"
            )

    else:

        formulario = DelegacionForm(
            instance=delegacion
        )

    contexto = {
        "formulario": formulario,
        "titulo": "Modificar delegación",
        "accion": "Guardar cambios",
        "delegacion": delegacion,
        "es_creacion": False,
    }

    return render(
        request,
        "delegaciones/formulario.html",
        contexto
    )


# =========================================================
# COMPROBAR RELACIONES DE UNA DELEGACION
# Evitar eliminar accidentalmente registros asociados
# =========================================================

def tiene_registros_relacionados(delegacion):

    for relacion in delegacion._meta.related_objects:

        modelo_relacionado = relacion.related_model

        campo_relacion = relacion.field.name

        filtros = {
            campo_relacion: delegacion
        }

        if modelo_relacionado._default_manager.filter(
            **filtros
        ).exists():
            return True

    return False


# =========================================================
# ELIMINAR DELEGACION
# Permiso: eliminar delegaciones
# Solo acepta solicitudes POST
# =========================================================

@login_required(login_url="login")
@permission_required(
    "delegacionesApp.delete_delegacion",
    raise_exception=True
)
@require_POST
def eliminar_delegacion(request, pk):

    delegacion = get_object_or_404(
        Delegacion,
        pk=pk
    )

    nombre = delegacion.nombre

    # Evitar eliminaciones de registros relacionados.
    if tiene_registros_relacionados(delegacion):

        messages.error(
            request,
            "No se puede eliminar esta delegación "
            "porque tiene registros relacionados."
        )

        return redirect(
            "inicio_delegaciones"
        )

    try:

        delegacion.delete()

        messages.success(
            request,
            f"La delegación '{nombre}' "
            "fue eliminada correctamente."
        )

    except (ProtectedError, RestrictedError):

        messages.error(
            request,
            "No se puede eliminar esta delegación "
            "porque existen registros asociados."
        )

    return redirect(
        "inicio_delegaciones"
    )
