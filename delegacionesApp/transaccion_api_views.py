
from rest_framework import serializers, status
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiResponse,
)

from .serializers import DelegacionSerializer
from .transaccion_serializers import RegistroConjuntoSerializer

from funcionariosApp.serializers import FuncionarioSerializer


# =========================================================
# SIGED EVA 4 - PERMISOS DE TRANSACCION RESTFUL
# =========================================================

class PermisosRegistroConjuntoAPI(BasePermission):
    """
    Solo permite registrar una delegacion con su
    funcionario inicial a usuarios que tengan
    ambos permisos de creacion.

    Se utilizan los permisos reales de Django.
    """

    message = (
        "No tienes permisos para crear una delegación "
        "y su funcionario inicial."
    )

    def has_permission(self, request, view):
        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        return (
            request.method == "POST"
            and usuario.has_perm(
                "delegacionesApp.add_delegacion"
            )
            and usuario.has_perm(
                "funcionariosApp.add_funcionario"
            )
        )


# =========================================================
# SIGED EVA 4 - TRANSACCION RESTFUL
# POST /api/delegaciones/registro-conjunto/
# =========================================================

class RegistroConjuntoAPI(APIView):
    """
    Registra una nueva delegacion y su funcionario inicial.

    Primero se validan todos los datos.

    El serializer realiza ambas inserciones dentro
    de una transaccion atomica, evitando registros
    parciales si ocurre un error durante el guardado.
    """

    permission_classes = [
        IsAuthenticated,
        PermisosRegistroConjuntoAPI,
    ]

    @extend_schema(
        tags=["Transacciones"],
        summary="Registrar delegación y funcionario inicial",
        description=(
            "Crea una delegación y su funcionario inicial "
            "en una sola transacción de base de datos. "
            "Requiere autenticación JWT y permisos de "
            "creación sobre ambas entidades."
        ),
        request=RegistroConjuntoSerializer,
        responses={
            201: OpenApiResponse(
                response=inline_serializer(
                    name="RegistroConjuntoRespuesta",
                    fields={
                        "mensaje": serializers.CharField(),
                        "delegacion": DelegacionSerializer(),
                        "funcionario": FuncionarioSerializer(),
                    },
                ),
                description=(
                    "Delegación y funcionario creados "
                    "correctamente."
                ),
            ),
            400: OpenApiResponse(
                description="Datos inválidos."
            ),
            401: OpenApiResponse(
                description="Autenticación requerida."
            ),
            403: OpenApiResponse(
                description="Permisos insuficientes."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Ejecuta el registro conjunto mediante JSON.
        """

        serializer = RegistroConjuntoSerializer(
            data=request.data
        )

        # Validar ambas entidades antes del guardado.
        serializer.is_valid(
            raise_exception=True
        )

        # El metodo create del serializer utiliza
        # transaction.atomic() para ambas inserciones.
        resultado = serializer.save()

        delegacion = resultado["delegacion"]
        funcionario = resultado["funcionario"]

        # Construir respuesta JSON con los registros.
        respuesta = {
            "mensaje": (
                "Delegación y funcionario inicial "
                "registrados correctamente."
            ),
            "delegacion": DelegacionSerializer(
                delegacion
            ).data,
            "funcionario": FuncionarioSerializer(
                funcionario
            ).data,
        }

        return Response(
            respuesta,
            status=status.HTTP_201_CREATED
        )
