
from django.urls import path

from .api_views import (
    FuncionarioListaCrearAPI,
    FuncionarioDetalleAPI,
)


# =========================================================
# SIGED EVA 4 - RUTAS API RESTFUL DE FUNCIONARIOS
# =========================================================

urlpatterns = [

    # =====================================================
    # LISTAR Y CREAR FUNCIONARIOS
    #
    # GET  /api/funcionarios/
    # POST /api/funcionarios/
    # =====================================================

    path(
        "",
        FuncionarioListaCrearAPI.as_view(),
        name="api_funcionarios_lista_crear"
    ),

    # =====================================================
    # CONSULTAR, MODIFICAR Y ELIMINAR FUNCIONARIO
    #
    # GET    /api/funcionarios/<id>/
    # PUT    /api/funcionarios/<id>/
    # PATCH  /api/funcionarios/<id>/
    # DELETE /api/funcionarios/<id>/
    # =====================================================

    path(
        "<int:pk>/",
        FuncionarioDetalleAPI.as_view(),
        name="api_funcionarios_detalle"
    ),

]
