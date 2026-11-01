
from django.urls import path
from . import views


# =========================================================
# SIGED EVA 3 - RUTAS DE FUNCIONARIOS
# =========================================================

urlpatterns = [

    # Listado y búsqueda de funcionarios
    path(
        '',
        views.inicio,
        name='inicio_funcionarios'
    ),

    # Ver detalle de un funcionario
    path(
        'detalle/<int:id>/',
        views.detalle,
        name='detalle_funcionario'
    ),

    # Registrar un nuevo funcionario
    path(
        'crear/',
        views.crear_funcionario,
        name='crear_funcionario'
    ),

    # Modificar un funcionario existente
    path(
        'editar/<int:id>/',
        views.editar_funcionario,
        name='editar_funcionario'
    ),

    # Eliminar un funcionario
    path(
        'eliminar/<int:id>/',
        views.eliminar_funcionario,
        name='eliminar_funcionario'
    ),

]
