
from django.urls import path

from . import views


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
    #
    # EVA 3:
    # Permite registrar opcionalmente un funcionario
    # inicial mediante una transaccion atomica.
    # =====================================================

    path(
        "crear/",
        views.crear_delegacion,
        name="crear_delegacion"
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
