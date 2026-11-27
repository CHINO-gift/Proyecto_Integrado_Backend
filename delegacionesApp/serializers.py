
from rest_framework import serializers

from .models import Delegacion


# =========================================================
# SIGED EVA 4 - SERIALIZER DE DELEGACIONES
# =========================================================

class DelegacionSerializer(serializers.ModelSerializer):
    """
    Convierte los registros de Delegacion a JSON y valida
    la informacion recibida mediante la API RESTful.

    Permite utilizar este serializer en las operaciones
    GET, POST y PUT/PATCH.
    """

    class Meta:
        model = Delegacion

        fields = [
            "id",
            "nombre",
            "sector",
            "descripcion",
        ]

        read_only_fields = [
            "id",
        ]

        extra_kwargs = {
            "nombre": {
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
                "max_length": 100,
            },
            "sector": {
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
                "max_length": 150,
            },
            "descripcion": {
                "required": True,
                "allow_blank": False,
                "trim_whitespace": True,
            },
        }

    # =====================================================
    # VALIDAR NOMBRE
    # =====================================================

    def validate_nombre(self, value):
        nombre = value.strip()

        if not nombre:
            raise serializers.ValidationError(
                "Debe ingresar el nombre de la delegación."
            )

        return nombre

    # =====================================================
    # VALIDAR SECTOR
    # =====================================================

    def validate_sector(self, value):
        sector = value.strip()

        if not sector:
            raise serializers.ValidationError(
                "Debe ingresar el sector de la delegación."
            )

        return sector

    # =====================================================
    # VALIDAR DESCRIPCION
    # =====================================================

    def validate_descripcion(self, value):
        descripcion = value.strip()

        if not descripcion:
            raise serializers.ValidationError(
                "Debe ingresar una descripción."
            )

        return descripcion
