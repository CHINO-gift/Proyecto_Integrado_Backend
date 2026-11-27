
from rest_framework import generics
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)

from .models import Funcionario
from .serializers import FuncionarioSerializer


# =========================================================
# SIGED EVA 4 - PERMISOS PARA API DE FUNCIONARIOS
# =========================================================

class PermisosFuncionarioAPI(BasePermission):
    """
    Controla las operaciones RESTful mediante
    los permisos configurados en Django.

    Administrador:
        GET, POST, PUT, PATCH y DELETE.

    Supervisor:
        GET, POST, PUT y PATCH.

    Administrativo:
        GET solamente.

    La autorizacion se comprueba en el servidor.
    """

    message = "No tienes permisos para realizar esta operación."

    def has_permission(self, request, view):
        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        permisos_por_metodo = {
            "GET": "view_funcionario",
            "HEAD": "view_funcionario",
            "OPTIONS": "view_funcionario",
            "POST": "add_funcionario",
            "PUT": "change_funcionario",
            "PATCH": "change_funcionario",
            "DELETE": "delete_funcionario",
        }

        permiso = permisos_por_metodo.get(request.method)

        if permiso is None:
            return False

        return usuario.has_perm(
            f"funcionariosApp.{permiso}"
        )


# =========================================================
# LISTAR Y CREAR FUNCIONARIOS
# GET /api/funcionarios/
# POST /api/funcionarios/
# =========================================================

class FuncionarioListaCrearAPI(generics.ListCreateAPIView):
    """
    GET:
        Retorna los funcionarios en formato JSON.

    POST:
        Permite registrar un funcionario
        asociado a una delegacion existente.
    """

    queryset = Funcionario.objects.select_related(
        "delegacion"
    ).all()

    serializer_class = FuncionarioSerializer

    permission_classes = [
        IsAuthenticated,
        PermisosFuncionarioAPI,
    ]


# =========================================================
# CONSULTAR, MODIFICAR Y ELIMINAR UN FUNCIONARIO
# GET /api/funcionarios/<id>/
# PUT /api/funcionarios/<id>/
# PATCH /api/funcionarios/<id>/
# DELETE /api/funcionarios/<id>/
# =========================================================

class FuncionarioDetalleAPI(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    GET:
        Consulta un funcionario.

    PUT:
        Modifica todos los campos editables.

    PATCH:
        Modifica solamente los campos enviados.

    DELETE:
        Elimina un funcionario, siempre que
        el usuario tenga el permiso correspondiente.
    """

    queryset = Funcionario.objects.select_related(
        "delegacion"
    ).all()

    serializer_class = FuncionarioSerializer

    permission_classes = [
        IsAuthenticated,
        PermisosFuncionarioAPI,
    ]
