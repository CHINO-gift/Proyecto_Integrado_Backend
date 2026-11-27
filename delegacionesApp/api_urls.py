
from django.urls import path

from .api_views import (
    DelegacionListaCrearAPI,
    DelegacionDetalleAPI,
)


# =========================================================
# SIGED EVA 4 - RUTAS API RESTFUL DE DELEGACIONES
# =========================================================

urlpatterns = [

    # GET: listar delegaciones
    # POST: crear delegacion
    path(
        "",
        DelegacionListaCrearAPI.as_view(),
        name="api_delegaciones_lista_crear"
    ),

    # GET: consultar delegacion
    # PUT/PATCH: modificar delegacion
    # DELETE: eliminar delegacion
    path(
        "<int:pk>/",
        DelegacionDetalleAPI.as_view(),
        name="api_delegaciones_detalle"
    ),

]
