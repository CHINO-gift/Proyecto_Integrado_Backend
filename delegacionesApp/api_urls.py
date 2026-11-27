
from django.urls import path

from .api_views import (
    DelegacionListaCrearAPI,
    DelegacionDetalleAPI,
)

from .transaccion_api_views import RegistroConjuntoAPI


# =========================================================
# SIGED EVA 4 - RUTAS API RESTFUL DE DELEGACIONES
# =========================================================

urlpatterns = [

    # =====================================================
    # LISTAR Y CREAR DELEGACIONES
    #
    # GET  /api/delegaciones/
    # POST /api/delegaciones/
    # =====================================================

    path(
        "",
        DelegacionListaCrearAPI.as_view(),
        name="api_delegaciones_lista_crear"
    ),

    # =====================================================
    # REGISTRO CONJUNTO DE DELEGACION Y FUNCIONARIO
    #
    # POST /api/delegaciones/registro-conjunto/
    # =====================================================

    path(
        "registro-conjunto/",
        RegistroConjuntoAPI.as_view(),
        name="api_delegaciones_registro_conjunto"
    ),

    # =====================================================
    # CONSULTAR, MODIFICAR Y ELIMINAR DELEGACIONES
    #
    # GET    /api/delegaciones/<id>/
    # PUT    /api/delegaciones/<id>/
    # PATCH  /api/delegaciones/<id>/
    # DELETE /api/delegaciones/<id>/
    # =====================================================

    path(
        "<int:pk>/",
        DelegacionDetalleAPI.as_view(),
        name="api_delegaciones_detalle"
    ),

]
