
from django.urls import path

from . import views


# =========================================================
# SIGED EVA 3 - RUTAS DE GESTION DE USUARIOS
# =========================================================

urlpatterns = [

    # =====================================================
    # LISTAR Y BUSCAR USUARIOS
    # =====================================================

    path(
        "",
        views.inicio,
        name="inicio_usuarios"
    ),

    # =====================================================
    # CREAR USUARIO
    # =====================================================

    path(
        "crear/",
        views.crear_usuario,
        name="crear_usuario"
    ),

    # =====================================================
    # MODIFICAR USUARIO
    # =====================================================

    path(
        "editar/<int:id>/",
        views.editar_usuario,
        name="editar_usuario"
    ),

]
