
from django.urls import path

from . import views
from . import views_operacion


# =========================================================
# SIGED EVA 3 - RUTAS DE DELEGACIONES
# =========================================================

urlpatterns = [

    # =====================================================
    # CONSULTAR DELEGACIONES
    # =====================================================

    path(
        "",
        views.inicio,
        name="inicio_delegaciones"
    ),

    path(
        "detalle/<str:nombre>/",
        views.detalle,
        name="detalle_delegacion"
    ),

    # =====================================================
    # AGREGAR DELEGACION
    # =====================================================

    path(
        "crear/",
        views.crear_delegacion,
        name="crear_delegacion"
    ),

    # =====================================================
    # EVA 3 - REGISTRO CONJUNTO
    # DELEGACION + FUNCIONARIO INICIAL
    # =====================================================
    #
    # Esta operacion registra dos entidades
    # relacionadas mediante transaction.atomic().
    #
    # Requiere permisos para crear delegaciones
    # y funcionarios.
    # =====================================================

    path(
        "registro-conjunto/",
        views_operacion.registrar_delegacion_con_funcionario,
        name="registro_conjunto"
    ),

    # =====================================================
    # MODIFICAR DELEGACION
    # =====================================================

    path(
        "editar/<int:pk>/",
        views.editar_delegacion,
        name="editar_delegacion"
    ),

    # =====================================================
    # ELIMINAR DELEGACION
    # =====================================================

    path(
        "eliminar/<int:pk>/",
        views.eliminar_delegacion,
        name="eliminar_delegacion"
    ),

]
