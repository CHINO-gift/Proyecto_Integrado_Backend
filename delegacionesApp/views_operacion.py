
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)

from django.db import transaction

from django.shortcuts import render, redirect

from django.views.decorators.http import require_http_methods

from .forms import DelegacionForm
from .forms_operacion import FuncionarioInicialForm


# =========================================================
# SIGED EVA 3 - TRANSACCION ENTRE DOS ENTIDADES
# =========================================================
#
# Operacion:
#
# 1. Registrar una nueva delegacion.
# 2. Registrar su funcionario inicial.
# 3. Relacionar ambas entidades.
#
# Los dos registros se guardan dentro de una
# misma transaccion mediante transaction.atomic().
#
# Si ocurre un error durante el guardado,
# Django revierte toda la operacion.
# =========================================================


# =========================================================
# REGISTRO CONJUNTO
# DELEGACION + FUNCIONARIO
# =========================================================

@login_required(login_url="login")
@permission_required(
    (
        "delegacionesApp.add_delegacion",
        "funcionariosApp.add_funcionario",
    ),
    raise_exception=True
)
@require_http_methods(["GET", "POST"])
def registrar_delegacion_con_funcionario(request):

    # =====================================================
    # FORMULARIOS
    # =====================================================
    #
    # Utilizamos prefijos porque ambos formularios
    # tienen un campo llamado "nombre".
    #
    # Esto evita conflictos entre sus datos.
    # =====================================================

    if request.method == "POST":

        formulario_delegacion = DelegacionForm(
            request.POST,
            prefix="delegacion"
        )

        formulario_funcionario = FuncionarioInicialForm(
            request.POST,
            prefix="funcionario"
        )

        # =================================================
        # VALIDAR AMBOS FORMULARIOS
        # =================================================

        delegacion_valida = (
            formulario_delegacion.is_valid()
        )

        funcionario_valido = (
            formulario_funcionario.is_valid()
        )

        if delegacion_valida and funcionario_valido:

            # =============================================
            # INICIO DE LA TRANSACCION
            # =============================================

            with transaction.atomic():

                # -----------------------------------------
                # 1. GUARDAR DELEGACION
                # -----------------------------------------

                delegacion = formulario_delegacion.save()

                # -----------------------------------------
                # 2. PREPARAR FUNCIONARIO
                # -----------------------------------------

                funcionario = formulario_funcionario.save(
                    commit=False
                )

                # -----------------------------------------
                # 3. ASOCIAR FUNCIONARIO A DELEGACION
                # -----------------------------------------

                funcionario.delegacion = delegacion

                # -----------------------------------------
                # 4. GUARDAR FUNCIONARIO
                # -----------------------------------------

                funcionario.save()

            # =============================================
            # TRANSACCION COMPLETADA
            # =============================================

            messages.success(
                request,
                (
                    f"La delegación '{delegacion.nombre}' "
                    f"y el funcionario '{funcionario.nombre}' "
                    "fueron registrados correctamente."
                )
            )

            return redirect(
                "inicio_delegaciones"
            )

        # Si alguno de los formularios no es valido,
        # no se guarda ninguna entidad.
        #
        # Los errores se mostraran en la plantilla HTML.

    else:

        # =================================================
        # MOSTRAR FORMULARIOS VACIOS
        # =================================================

        formulario_delegacion = DelegacionForm(
            prefix="delegacion"
        )

        formulario_funcionario = FuncionarioInicialForm(
            prefix="funcionario"
        )

    # =====================================================
    # CONTEXTO
    # =====================================================

    contexto = {

        "titulo": (
            "Registrar delegación y funcionario"
        ),

        "formulario_delegacion": (
            formulario_delegacion
        ),

        "formulario_funcionario": (
            formulario_funcionario
        ),
    }

    # =====================================================
    # MOSTRAR PLANTILLA
    # =====================================================

    return render(
        request,
        "delegaciones/registro_conjunto.html",
        contexto
    )
