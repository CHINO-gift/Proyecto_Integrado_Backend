
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import Delegacion
from .serializers import DelegacionSerializer


# =========================================================
# SIGED EVA 4 - PERMISOS PARA API DE DELEGACIONES
# =========================================================

class PermisosDelegacionAPI(BasePermission):
    """
    Controla las operaciones permitidas para cada usuario.

    Administrador: consultar, crear, editar y eliminar.
    Supervisor: consultar, crear y editar.
    Administrativo: solamente consultar.

    Los permisos se validan en el servidor, no solamente
    ocultando botones de la interfaz.
    """

    message = "No tienes permisos para realizar esta operación."

    def has_permission(self, request, view):
        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        metodo = request.method

        permisos_por_metodo = {
            "GET": "view_delegacion",
            "HEAD": "view_delegacion",
            "OPTIONS": "view_delegacion",
            "POST": "add_delegacion",
            "PUT": "change_delegacion",
            "PATCH": "change_delegacion",
            "DELETE": "delete_delegacion",
        }

        permiso = permisos_por_metodo.get(metodo)

        if permiso is None:
            return False

        return usuario.has_perm(
            f"delegacionesApp.{permiso}"
        )


# =========================================================
# LISTAR Y CREAR DELEGACIONES
# GET /api/delegaciones/
# POST /api/delegaciones/
# =========================================================

class DelegacionListaCrearAPI(generics.ListCreateAPIView):
    """
    GET: devuelve todas las delegaciones en JSON.
    POST: registra una nueva delegacion.
    """

    queryset = Delegacion.objects.all()
    serializer_class = DelegacionSerializer

    permission_classes = [
        IsAuthenticated,
        PermisosDelegacionAPI,
    ]


# =========================================================
# CONSULTAR, MODIFICAR Y ELIMINAR UNA DELEGACION
# GET /api/delegaciones/<id>/
# PUT /api/delegaciones/<id>/
# PATCH /api/delegaciones/<id>/
# DELETE /api/delegaciones/<id>/
# =========================================================

class DelegacionDetalleAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: consulta una delegacion.
    PUT/PATCH: modifica sus datos.
    DELETE: elimina una delegacion.
    """

    queryset = Delegacion.objects.all()
    serializer_class = DelegacionSerializer

    permission_classes = [
        IsAuthenticated,
        PermisosDelegacionAPI,
    ]
